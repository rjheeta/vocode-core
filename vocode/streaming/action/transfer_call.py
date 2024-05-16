import os
from typing import Type
from pydantic.v1 import BaseModel, Field
from twilio.rest import Client

from vocode.streaming.action.phone_call_action import TwilioPhoneCallAction
from vocode.streaming.models.actions import (
    ActionConfig,
    ActionInput,
    ActionOutput,
    ActionType,
)

class TransferCallActionConfig(ActionConfig, type=ActionType.TRANSFER_CALL):
    pass

class TransferCallParameters(BaseModel):
    to_phone: str = Field(..., description="phone number to transfer the call to")

class TransferCallResponse(BaseModel):
    status: str = Field("success", description="status of the transfer")

class TransferCall(
    TwilioPhoneCallAction[
        TransferCallActionConfig, TransferCallParameters, TransferCallResponse
    ]
):
    description: str = "transfers the call. use when you need to connect the active call to another phone line."
    parameters_type: Type[TransferCallParameters] = TransferCallParameters
    response_type: Type[TransferCallResponse] = TransferCallResponse

    async def transfer_call(self, twilio_call_sid, to_phone):
        twilio_account_sid = os.environ["TWILIO_ACCOUNT_SID"]
        twilio_auth_token = os.environ["TWILIO_AUTH_TOKEN"]
        client = Client(twilio_account_sid, twilio_auth_token)

        twiml = f"<Response><Dial>{to_phone}</Dial></Response>"
        call = client.calls(twilio_call_sid).update(twiml=twiml)
        
        return call

    async def run(
        self, action_input: ActionInput[TransferCallParameters]
    ) -> ActionOutput[TransferCallResponse]:
        twilio_call_sid = self.get_twilio_sid(action_input)
        await self.transfer_call(twilio_call_sid, action_input.params.to_phone)
        return ActionOutput(
            action_type=action_input.action_config.type,
            response=TransferCallResponse(status="success"),
        )
