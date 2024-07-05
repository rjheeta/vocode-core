from vocode.streaming.input_device.file_input_device import FileInputDevice
from vocode.streaming.input_device.microphone_input import MicrophoneInput
from vocode.streaming.models.transcriber import DeepgramTranscriberConfig, Transcription
from vocode.streaming.transcriber.base_transcriber import BaseTranscriber
from vocode.streaming.transcriber.deepgram_transcriber import (
    DeepgramEndpointingConfig,
    DeepgramTranscriber,
)

if __name__ == "__main__":
    import asyncio

    from dotenv import load_dotenv

    load_dotenv()

    async def print_output(transcriber: BaseTranscriber):
        while True:
            transcription: Transcription = await transcriber.output_queue.get()
            print(transcription)

    async def listen():
        input_device = MicrophoneInput.from_default_device()
        # input_device = FileInputDevice(file_path="spacewalk.wav")

        # replace with the transcriber you want to test
        transcriber = DeepgramTranscriber(
            DeepgramTranscriberConfig.from_input_device(
                input_device, endpointing_config=DeepgramEndpointingConfig()
            )
        )
        transcriber.start()
        asyncio.create_task(print_output(transcriber))
        print("Start speaking...press Ctrl+C to end. ")
        while True:
            chunk = await input_device.get_audio()
            transcriber.send_audio(chunk)

    asyncio.run(listen())
