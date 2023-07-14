import os
import torch
from img2img import StableDiffusionXLImg2ImgPipeline


class DeforumDiffusion:
    def __init__(
        self,
        model_name="stabilityai/stable-diffusion-xl-base-0.9",
        dtype=torch.float16,
        variant="fp16",
        use_safetensors=True,
        device="cuda",
        sample_dir="samples",
        sample_format="sample_{:05d}.png",
    ):
        self.model_name = model_name
        self.dtype = dtype
        self.variant = variant
        self.use_safetensors = use_safetensors
        self.device = device
        self.sample_dir = sample_dir
        self.sample_format = sample_format

        self.pipe = StableDiffusionXLImg2ImgPipeline.from_pretrained(
            model_name,
            torch_dtype=dtype,
            variant=variant,
            use_safetensors=use_safetensors,
        )
        self.pipe.to(device)

        if not os.path.exists(self.sample_dir):
            os.makedirs(self.sample_dir)

    def generate(self, prompt, width=1024, height=1024, max_frames=40, strength=0.5, init=None):
        strength = 1
        for iframe in range(max_frames):
            image, init = self.pipe(
                prompt=prompt, width=width, height=height, image=init, strength=strength
            )
            strength = 0.55
            image.save(os.path.join(self.sample_dir, self.sample_format.format(iframe+1)))


# Create an instance of the DeforumDiffusion class
dd = DeforumDiffusion()

# Use d instance to call generate function with the values prompt,max_frames and strength
dd.generate(
    prompt="Mystical Interpretations of Hokusai's Dragon: Katsushika's Iconic Serpent Reimagined in Vibrant Surrealist Charcoal",
    max_frames=80,
    strength=0.5,
)
