import torch
import PIL
from torchvision import transforms

def load_image(image_obj, device='cpu', resolution=None):
    if type(image_obj) == str:
        pil_image = PIL.Image.open(image_obj)
    elif type(image_obj) == PIL.Image.Image:
        pil_image = image_obj
    else:
        raise ValueError(f"Unrecognized image type: {type(image_obj)}")
    if resolution is not None:
        transform = transforms.Compose([
            transforms.ToTensor(),
            transforms.Resize((resolution, resolution))
        ])
    else:
        transform = transforms.Compose([
            transforms.ToTensor()
        ])
    tensor_image = transform(pil_image)
    return torch.unsqueeze(tensor_image, 0).to(device)


def save_image(images, image_path, down_factor=None,
               caption=None, font_size=40, text_color=(255, 255, 255), image_type="RGB"):
    image_np = (images * 127.5 + 128).clip(0, 255).to(torch.uint8).permute(1, 2, 0).cpu().numpy()
    if image_np.shape[2] == 1:
        pil_image = PIL.Image.fromarray(image_np[:, :, 0], 'L')
    else:
        pil_image = PIL.Image.fromarray(image_np, image_type)
    if down_factor is not None:
        pil_image = pil_image.resize((pil_image.size[0] // down_factor, pil_image.size[1] // down_factor))
    
    if caption is not None:
        draw = PIL.ImageDraw.Draw(pil_image)
        # use LaTeX bold font
        font = PIL.ImageFont.truetype("cmr10.ttf", font_size)
        # make bold
        draw.text((0, 0), caption, text_color, font=font)

    pil_image.save(image_path)

