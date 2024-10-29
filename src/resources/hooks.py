from dagster import (failure_hook, 
                     success_hook, 
                     HookContext,
                     HookDefinition)
from dagster._core.definitions.decorators.hook_decorator import (SuccessOrFailureHookFn,
                                                                 HookExecutionResult,
                                                                 _validate_hook_fn_params,
                                                                 event_list_hook)
from dagster._core.events import DagsterEvent
from typing import Callable, Optional, Union, AbstractSet, Sequence
import dagster._check as check

def skipped_hook(
    hook_fn: Optional[SuccessOrFailureHookFn] = None,
    *,
    name: Optional[str] = None,
    required_resource_keys: Optional[AbstractSet[str]] = None,
) -> Union[HookDefinition, Callable[[SuccessOrFailureHookFn], HookDefinition]]:
    """Customized version of success_hook or failure_hook decorator (Dagster's built-in).

    Args:
        name (Optional[str]): The name of this hook.
        required_resource_keys (Optional[AbstractSet[str]]): Keys for the resources required by the
            hook.

    Examples:
        .. code-block:: python

            @skipped_hook(required_resource_keys={'slack'})
            def slack_message_on_skipped(context):
                message = 'op {} succeeded'.format(context.op.name)
                context.resources.slack.send_message(message)

            @skipped_hook
            def do_something_on_success(context):
                do_something()


    """

    def wrapper(fn: SuccessOrFailureHookFn) -> HookDefinition:
        check.callable_param(fn, "fn")

        expected_positionals = ["context"]
        _validate_hook_fn_params(fn, expected_positionals)

        if name is None or callable(name):
            _name = fn.__name__
        else:
            _name = name

        @event_list_hook(name=_name, required_resource_keys=required_resource_keys, decorated_fn=fn)
        def _skipped_hook(
            context: "HookContext", event_list: Sequence["DagsterEvent"]
        ) -> HookExecutionResult:
            for event in event_list:
                if event.is_step_skipped:
                    fn(context)
                    return HookExecutionResult(hook_name=_name, is_skipped=False)

            # hook is skipped when fn didn't run
            return HookExecutionResult(hook_name=_name, is_skipped=True)

        return _skipped_hook

    # This case is for when decorator is used bare, without arguments, i.e. @success_hook
    if hook_fn is not None:
        check.invariant(required_resource_keys is None)
        return wrapper(hook_fn)

    return wrapper


def create_skipped_hook_via_slack(channel_id: str = "#data-pipeline-alert") -> HookDefinition:
    @skipped_hook(required_resource_keys={"slack"})
    def slack_message_hook(context: HookContext):
        message = f"Op {context.step_key} ({context.job_name}) has been skipped"
        context.resources.slack.chat_postMessage(channel=channel_id, text=message)
    
    return slack_message_hook

def create_success_hook_via_slack(channel_id: str = "#data-pipeline-alert") -> HookDefinition:
    @success_hook(required_resource_keys={"slack"})
    def slack_message_hook(context: HookContext):
        message = f"Op {context.job_name} finished successfully"
        context.resources.slack.chat_postMessage(channel=channel_id, text=message)
    
    return slack_message_hook

def create_failure_hook_via_slack(channel_id: str = "#data-pipeline-alert") -> HookDefinition:
    @failure_hook(required_resource_keys={"slack"})
    def slack_message_hook(context: HookContext):
        message = f"Op {context.job_name} failed ({context.op_exception})"
        context.resources.slack.chat_postMessage(channel=channel_id, text=message)
    
    return slack_message_hook