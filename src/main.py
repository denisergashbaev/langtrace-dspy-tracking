from dspy_modules import advice_generator
from loguru import logger
from langtrace_python_sdk.utils.with_root_span import with_langtrace_root_span
from langtrace_python_sdk import inject_additional_attributes

import getpass


@with_langtrace_root_span(name="run_contextvars")
def run_with_contextvars():
    desired_objectives = ["Become a better programmer", "Become excellent data scientist"]
    simple_advices = advice_generator.AdviceGenerator.run_in_context(desired_objectives)
    for idx, simple_advice in enumerate(simple_advices):
        logger.info(f"{idx}: {simple_advice}")


@with_langtrace_root_span(name="run_no_contextvars")
def run_no_contextvars():
    desired_objectives = ["Become a top-notch cook", "Become a farmer"]
    simple_advices = advice_generator.AdviceGenerator.run_in_context_no_contextvars(desired_objectives)
    for idx, simple_advice in enumerate(simple_advices):
        logger.info(f"{idx}: {simple_advice}")


@with_langtrace_root_span(name="run_with_opentelemetry")
def run_opentelemetry():
    desired_objectives = ["Become good at yoga", "Become good at aikido"]
    simple_advices = advice_generator.AdviceGenerator.run_in_context_no_contextvars(desired_objectives)
    for idx, simple_advice in enumerate(simple_advices):
        logger.info(f"{idx}: {simple_advice}")


if __name__ == '__main__':
    additional_vars = {'user_id': getpass.getuser()}
    inject_additional_attributes(lambda: run_with_contextvars(), additional_vars)
    inject_additional_attributes(lambda: run_no_contextvars(), additional_vars)
    inject_additional_attributes(lambda: run_opentelemetry(), additional_vars)


