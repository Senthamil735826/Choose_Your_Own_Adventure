from typing import Any, cast
from sqlalchemy.orm import Session

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from core.config import settings
from core.models import StoryLLMResponse, StoryNodeLLM
from core.prompts import STORY_PROMPT
from models.story import Story, StoryNode
from dotenv import load_dotenv

load_dotenv()

class StoryGenerator:

    @classmethod
    def _get_llm(cls):
        return ChatGoogleGenerativeAI(
    model="gemini-3-flash-preview",
    google_api_key=settings.GEMINI_API_KEY

    )

    @classmethod
    def generate_story(
        cls,
        db: Session,
        session_id: str,
        theme: str = "fantasy"
    ) -> Story:

        llm = cls._get_llm()

        story_parser = PydanticOutputParser(
            pydantic_object=StoryLLMResponse
        )

        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", STORY_PROMPT),
                ("human", "Create the story with this theme: {theme}")
            ]
        ).partial(
            format_instructions=story_parser.get_format_instructions()
        )

        formatted_prompt = prompt.invoke({"theme": theme})

        raw_response = llm.invoke(formatted_prompt)

        response_text = (
            raw_response.content
            if hasattr(raw_response, "content")
            else str(raw_response)
        )

        if isinstance(response_text, list):
            parts = []
            for part in response_text:
                if isinstance(part, str):
                    parts.append(part)
                elif isinstance(part, dict) and "text" in part:
                    parts.append(part["text"])
                else:
                    parts.append(str(part))
            response_text = "".join(parts)

        if not isinstance(response_text, str):
            response_text = str(response_text)

        story_structure = story_parser.parse(response_text)

        story_db = Story(
            title=story_structure.title,
            session_id=session_id
        )

        db.add(story_db)
        db.flush()

        root_node = story_structure.rootNode

        if isinstance(root_node, dict):
            root_node = StoryNodeLLM.model_validate(root_node)

        cls._process_story_node(
            db=db,
            story_id=cast(int, story_db.id),
            node_data=root_node,
            is_root=True
        )

        db.commit()
        db.refresh(story_db)

        return story_db

    @classmethod
    def _process_story_node(
        cls,
        db: Session,
        story_id: int,
        node_data: StoryNodeLLM,
        is_root: bool = False
    ) -> StoryNode:

        node = StoryNode(
            story_id=story_id,
            content=node_data.content,
            is_root=is_root,
            is_ending=node_data.isEnding,
            is_winning_ending=node_data.isWinningEnding,
            options=[]
        )

        db.add(node)
        db.flush()

        if (
            not node.is_ending
            and hasattr(node_data, "options")
            and node_data.options
        ):

            options_list = []

            for option_data in node_data.options:

                next_node = option_data.nextNode

                if next_node is None:
                    continue

                if isinstance(next_node, dict):
                    next_node = StoryNodeLLM.model_validate(next_node)

                child_node = cls._process_story_node(
                    db=db,
                    story_id=story_id,
                    node_data=next_node,
                    is_root=False
                )

                options_list.append(
                    {
                        "text": option_data.text,
                        "node_id": cast(int, child_node.id)
                    }
                )

            node.options = cast(Any, options_list)
            db.flush()

        return node
