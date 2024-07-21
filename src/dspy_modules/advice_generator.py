import contextvars
import traceback
from concurrent.futures import ThreadPoolExecutor

import dspy
from loguru import logger
import pydantic
from src import config


class SimpleAdvice(pydantic.BaseModel):
    lifestyle_modifications: str = pydantic.Field(description="Lifestyle modifications")
    dietary_recommendations: str = pydantic.Field(description="Dietary recommendations")
    other_recommendations: str = pydantic.Field(description="Other recommendations")


class AdviceSignature(dspy.Signature):
    """Generate advice for a user to improve desired objective"""
    desired_objective: str = dspy.InputField(
        desc="Desired objective",
    )
    simple_advice: SimpleAdvice = dspy.OutputField(
        desc="Simple advice",
    )


class AdviceGenerator(dspy.Module):
    def __init__(self) -> None:
        super().__init__()
        self.program = dspy.functional.TypedChainOfThought(
            signature=AdviceSignature,
        )

    def forward(
        self,
        desired_objective: str,
    ) -> dspy.Prediction:
        return self.program(
            desired_objective=desired_objective,
        )

    @staticmethod
    def _run(
        desired_objective: str
    ) -> dspy.Prediction:
        with dspy.context(lm=config.lm):
            advice_generator = AdviceGenerator()
            return advice_generator.forward(
                desired_objective=desired_objective,
            )

    @staticmethod
    def run_in_context(
        desired_objectives: list[str],
    ) -> list[SimpleAdvice]:
        futures = []
        with ThreadPoolExecutor() as executor:
            for desired_objective in desired_objectives:
                futures.append(  # noqa: PERF401
                    executor.submit(
                        contextvars.copy_context().run,
                        AdviceGenerator._run,
                        desired_objective=desired_objective,
                    ),
                )
        simple_advices: list[SimpleAdvice] = []
        for future in futures:
            if exception := future.exception():
                logger.error(
                    "\n".join(
                        traceback.format_exception(
                            type(exception), exception, exception.__traceback__
                        )
                    )
                )
                continue
            simple_advices.append(future.result().simple_advice)
        logger.debug(f"Generated section consultations: {simple_advices=}")
        return simple_advices
