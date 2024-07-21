from dspy_modules import advice_generator
from loguru import logger
from langtrace_python_sdk.utils.with_root_span import with_langtrace_root_span
from langtrace_python_sdk import inject_additional_attributes

import getpass


@with_langtrace_root_span(name="run_single_trace")
def run_single_trace():
    desired_objectives = ["Become a better programmer", "Become excellent data scientist"]
    simple_advices = advice_generator.AdviceGenerator.run_in_context(desired_objectives)
    for idx, simple_advice in enumerate(simple_advices):
        logger.info(f"{idx}: {simple_advice}")


if __name__ == '__main__':
    inject_additional_attributes(run_single_trace, {'user_id': getpass.getuser()})


