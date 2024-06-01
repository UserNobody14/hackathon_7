import os
import elevenlabs
import assemblyai as aai

from dotenv import load_dotenv
from moviepy.editor import VideoFileClip, concatenate_videoclips, CompositeVideoClip, AudioFileClip, TextClip, ColorClip
from moviepy.video.tools.subtitles import SubtitlesClip
from elevenlabs import Voice, VoiceSettings
from elevenlabs.client import ElevenLabs

class ContentError(Exception):
    """Exception raised for errors in the ContentProducer class."""
    pass

class ContentProducer: 
    """A class for producing content from provided content data."""

    def __init__(self):
        """Initializes the ContentProducer."""
        load_dotenv()
        self.assembly_ai_api_key = os.environ.get("ASSEMBLY_AI_API_KEY")
        self.eleven_labs_api_key = os.environ.get("ELEVEN_LABS_API_KEY")
        self.client = ElevenLabs(api_key=self.eleven_labs_api_key)
        self.aai = aai.settings.api_key = self.assembly_ai_api_key

    def invoke(self, content_data):
        """Invokes the content production process.

        Args:
            content_data (list): A list of ContentData objects containing script and montage URL.

        Raises:
            ContentError: An error occurred during the content production process.
        """
        try:
            self._create_voice_over(content_data)
            self._create_video_short(content_data)
        except Exception as e:
            raise ContentError("Error creating content: " + str(e))
        return 

    def _create_voice_over(self, content_data):
            """Creates voice-over text-to-speech (TTS) audio files and subtitles.

            Args:
                content_data (list): A list of ContentData objects containing script and montage URL.
            """
            for i, data in enumerate(content_data):
                if data.category == 'tech_science':
                    script = f"What's going on in tech today?\n\n" + data.script
                else:
                     script = f"What's going on in {data.category} today?\n\n" + data.script

                audio_file_name = f'audio_clip_{i}.mp3' 
                audio = self.client.generate(
                    text=script, 
                    voice=Voice(
                        voice_id='yeNojDSkqjMLki231UWs',
                        settings=VoiceSettings(stability=0.5, similarity_boost=0.75)
                    ),
                    model="eleven_turbo_v2"
                )
                elevenlabs.save(audio, audio_file_name)

                transcript = aai.Transcriber().transcribe(audio_file_name)
                print("Transcript: ", transcript.text)
                subtitles = transcript.export_subtitles_srt(chars_per_caption=20)

                with open(f"subtitles_{i}.srt", "w") as file:
                    file.write(subtitles)

    def _create_video_short(self, content_data):
            """Creates short video clips with text-to-speech (TTS) audio and subtitles.

            Args:
                content_data (list): A list of ContentData objects containing script and montage URL.
            """
            for i, (data) in enumerate(content_data):
                montage_url = data.montage_url
                
                filename = f'audio_clip_{i}.mp3' 
                narration_audio = AudioFileClip(filename)
                audio_duration = narration_audio.duration

                def generator(txt, duration):
                    """Generates a video clip with centered text over a clip mathcing the topic category.

                    Args:
                        txt (str): The subtitle text.
                        duration (float): Duration of the subtitle text display.

                    Returns:
                        CompositeVideoClip: A video clip with the subtitle text and background.
                    """
                    font_size = 40
                    dummy_clip = TextClip(txt, font="Arial-Bold", fontsize=font_size) # Create a dummy TextClip to measure text size
                    text_width, text_height = dummy_clip.size
                    
                    padding_x = 20
                    padding_y = 10
                    bg_width = text_width + padding_x * 2
                    bg_height = text_height + padding_y * 2

                    return CompositeVideoClip([
                        ColorClip((bg_width, bg_height), color=(0, 0, 0)).set_opacity(0.5).set_duration(duration), 
                        TextClip(
                            txt,
                            font="Arial-Bold",
                            fontsize=font_size,
                            color='white',
                            align='center',
                            size=(bg_width, None),  # Set width, let height adjust dynamically
                        ).set_position(('center', 'center')).set_duration(duration)
                    ])

                subtitles_clip = SubtitlesClip(f"subtitles_{i}.srt", lambda txt, duration=audio_duration: generator(txt, duration))

                video_clip = VideoFileClip(montage_url)
                video_duration = video_clip.duration

                if video_duration < audio_duration:
                    repeated_video_clip = video_clip.loop(duration=audio_duration)
                    adjusted_video_clip = repeated_video_clip
                elif video_duration > audio_duration:
                    adjusted_video_clip = video_clip.subclip(0, audio_duration)
                
                final_with_subtitles = adjusted_video_clip.set_audio(narration_audio).set_duration(adjusted_video_clip.duration)
                final_with_subtitles = CompositeVideoClip([
                    final_with_subtitles,
                    subtitles_clip.set_pos("center")
                ])

                outro_audio = AudioFileClip("outro_audio.mp3")   
                outro_clip = VideoFileClip("outro_clip.mp4").set_audio(outro_audio)

                clip_array=[final_with_subtitles, outro_clip]

                final_short = concatenate_videoclips(clip_array)
                final_short.write_videofile(f"final_clip_{i}.mp4", fps=24)