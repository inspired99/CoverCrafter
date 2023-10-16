from ..prompt_translator.translation import TranslatorModel
from diffusers import AutoPipelineForText2Image

import torch


class DiffusionModel:
    """
    Diffusion Text2Image Model for generating images via prompt - Kandinsky 2.2
    """

    def __init__(self):
        self.model_path = "kandinsky-community/kandinsky-2-2-decoder"
        self.generation_pipeline = AutoPipelineForText2Image.from_pretrained(self.model_path, torch_dtype=torch.float16)
        self.device = 'cuda:1' if torch.cuda.is_available() else 'cpu'
        self.default_negative_prompt = (
            'low resolution, text, error, cropped, worst quality, low quality, jpeg artifacts,'
            'ugly, duplicate, morbid, mutilated, out of frame, mutated hands,'
            'poorly drawn hands, poorly drawn face, mutation, deformed, blurry, bad anatomy,'
            'bad proportions, missing arms, missing legs')
        self.generation_pipeline.to(self.device)
        self.translator = TranslatorModel()

    def generate_image(self, prompt_keywords, height=800, width=800, prior_guidance_scale=1.0,
                       negative_prompt=None):

        if negative_prompt is None:
            negative_prompt = self.default_negative_prompt
        else:
            negative_prompt = self.translator.translate(negative_prompt)

        prompt = ', '.join(prompt_keywords)
        translated_prompt = self.translator.translate(prompt)

        return self.generation_pipeline(prompt=translated_prompt, negative_prompt=negative_prompt,
                                        prior_guidance_scale=prior_guidance_scale,
                                        height=height, width=width).images[0]
