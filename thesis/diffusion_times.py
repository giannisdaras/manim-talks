from manim import *
from manim_slides import Slide
from utils import load_image, save_image
import torch
from manim_mobject_svg import *
import os
os.makedirs("assets/svgs", exist_ok=True)

color_profiles = {
    "dark": {
        "circle": "#FFFFFF", # white
        "line": "#FFFFFF", # white
    },
    "light": {
        "circle": "#000000",
        "line": "#000000",
    }
}


class TalkOutline(Slide):
    """Create a line to represent the diffusion process."""
    def construct(self, color_profile="dark", line_length=16, circle_radius=0.2):
        horizontal_line = Line(start=[-line_length / 2., 0, 0], end=[line_length / 2., 0, 0], color=color_profiles[color_profile]["line"])
        self.add(horizontal_line)
        self.play(Create(horizontal_line))

        # add 5 circles to the line, equally spaced.
        circles = VGroup()
        # create a linspace of 4 points between -line_length and line_length
        circle_positions = np.linspace(16 * circle_radius, line_length, num=5)
        for i in range(4):
            circle = Circle(radius=circle_radius, color=color_profiles[color_profile]["circle"])
            circle.move_to(horizontal_line.get_left() + RIGHT * circle_positions[i])
            circles.add(circle)
        
        self.play(Create(circles))
        self.next_slide()

        # add vertical lines on top of each circle
        vertical_lines = VGroup()
        for index, circle in enumerate(circles):
            if index % 2 == 0:
                line = Line(start=circle.get_top(), end=circle.get_top() + UP, color=color_profiles[color_profile]["line"])
                vertical_lines.add(line)
            else:
                line = Line(start=circle.get_bottom(), end=circle.get_bottom() + DOWN, color=color_profiles[color_profile]["line"])
                vertical_lines.add(line)
        

        # add text labels to the vertical lines
        text_labels = ["Additive noise", "Partially noisy data", "Linear Measurements", "General Corruptions"]
        labels = VGroup()
        for index, line in enumerate(vertical_lines):
            label = Text(text_labels[index], color=color_profiles[color_profile]["line"])
            labels.add(label)
        # move labels on top of the vertical lines
        for index, (label, line) in enumerate(zip(labels, vertical_lines)):
            if index % 2 == 0:
                label.next_to(line, UP)
            else:
                label.next_to(line, DOWN)
        
        slide_vgroup = VGroup(circles, vertical_lines, horizontal_line, labels)        
        slide_vgroup.to_svg("assets/svgs/outline.svg")

        # self.play(Create(vertical_lines))
        # self.next_slide()



class DiffusionLine(Slide):
    """Create a line to represent the diffusion process."""
    def construct(self):
        line = Line(start=[-4, 0, 0], end=[4, 0, 0], color=BLUE)
        self.add(line)
        self.play(Create(line))
        self.next_slide()        # Add xticks to the line
        tick_positions = np.linspace(-4, 4, num=9)
        ticks = VGroup()
        for pos in tick_positions:
            tick = Line(start=[pos, -0.1, 0], end=[pos, 0.1, 0], color=WHITE)
            ticks.add(tick)
        self.add(ticks)

        self.play(Create(ticks))
        self.next_slide()
        # add labels for the leftmost and rightmost ticks
        left_label = MathTex("T").next_to(tick_positions[0] * RIGHT, DOWN)
        right_label = MathTex("0").next_to(tick_positions[-1] * RIGHT, DOWN)
        self.play(Write(left_label), Write(right_label))
        self.next_slide()
        # # add a vertical dashed line to the leftmost and rightmost ticks
        # left_dashed_line = DashedLine(start=[-4, -3, 0], end=[-4, 3, 0], color=BLUE)
        # right_dashed_line = DashedLine(start=[4, -3, 0], end=[4, 3, 0], color=BLUE)
        # self.play(Create(left_dashed_line), Create(right_dashed_line))
        # self.next_slide()
        # Add two horizontal arrows with 'Diffusion Time' text between them below the line
        diffusion_time_text = Text("Diffusion Time")
        arrow_left = Arrow(start=diffusion_time_text.get_left(), end=line.get_left(), color=WHITE)
        arrow_right = Arrow(start=diffusion_time_text.get_right(), end=line.get_right(), color=WHITE)
        diffusion_group = VGroup(arrow_left, diffusion_time_text, arrow_right).next_to(line, 4 * DOWN)
        self.play(Write(diffusion_group))
        self.next_slide()
        clean_image = load_image("assets/clean_image.jpg") * 2 - 1

        # Add image to the slide
        image = ImageMobject("assets/clean_image.jpg").scale(0.25)  # Scale down the image to fit better
        image.next_to(line.get_right(), 2 * UP)  # Position the image above the right end of the line
        self.play(FadeIn(image))
        self.next_slide()
        # add gaussian noise to the image at 3 different scales
        noise = torch.randn_like(clean_image)
        noisy_image_1 = clean_image + noise * 1.0
        noisy_image_2 = clean_image + noise * 2.0
        noisy_image_3 = clean_image + noise * 5.0

        # Convert noisy images from tensors to PIL images and save them
        image_1_path = "assets/noisy_image_1.png"
        save_image(noisy_image_1.squeeze(0), image_1_path)
        image_2_path = "assets/noisy_image_2.png"
        save_image(noisy_image_2.squeeze(0), image_2_path)

        image_3_path = "assets/noisy_image_3.png"
        save_image(noisy_image_3.squeeze(0), image_3_path)

        image_4_path = "assets/noisy_image_4.png"
        save_image(noise.squeeze(0), image_4_path)

        # Add images to the slide
        image_1 = ImageMobject(image_1_path).scale(0.25)
        image_2 = ImageMobject(image_2_path).scale(0.25)
        image_3 = ImageMobject(image_3_path).scale(0.25)

        # Distribute images horizontally along the line
        image_2.next_to(line, 2 * UP)  # Place image_2 in the center of the line
        image_1.next_to(image_2, 1.5 * RIGHT)  # Place image_1 to the right of image_2
        image_3.next_to(image_2, 1.5 * LEFT)  # Place image_3 to the left of image_2
        
        image4 = ImageMobject(image_4_path).scale(0.25).next_to(line.get_left(), 2 * UP)

        # Add images to the slide with a fade-in animation
        self.play(FadeIn(image_1))
        self.next_slide()

        self.play(FadeIn(image_2))
        self.next_slide()

        self.play(FadeIn(image_3))
        self.next_slide()

        self.play(FadeIn(image4))
        self.next_slide()


        # add curved arrows from one image to the next one
        arrow0 = CurvedArrow(start_point=image.get_top() + 0.2 * UP, end_point=image_1.get_top() + 0.2 * UP, color=WHITE)
        arrow1 = CurvedArrow(start_point=image_1.get_top() + 0.2 * UP, end_point=image_2.get_top() + 0.2 * UP, color=WHITE)
        arrow2 = CurvedArrow(start_point=image_2.get_top() + 0.2 * UP, end_point=image_3.get_top() + 0.2 * UP, color=WHITE)
        arrow3 = CurvedArrow(start_point=image_3.get_top() + 0.2 * UP, end_point=image4.get_top() + 0.2 * UP, color=WHITE)
        self.play(Create(arrow0), Create(arrow1), Create(arrow2), Create(arrow3))
        self.next_slide()



class ManyCleanImages(Slide):
    """Create a line to represent the diffusion process."""
    def construct(self):
        line = Line(start=[-4, 0, 0], end=[4, 0, 0], color=BLUE)
        self.add(line)
        self.play(Create(line))
        self.next_slide()        # Add xticks to the line
        tick_positions = np.linspace(-4, 4, num=9)
        ticks = VGroup()
        for pos in tick_positions:
            tick = Line(start=[pos, -0.1, 0], end=[pos, 0.1, 0], color=WHITE)
            ticks.add(tick)
        self.add(ticks)

        self.play(Create(ticks))
        self.next_slide()
        # add labels for the leftmost and rightmost ticks
        left_label = MathTex("T").next_to(tick_positions[0] * RIGHT, DOWN)
        right_label = MathTex("0").next_to(tick_positions[-1] * RIGHT, DOWN)
        self.play(Write(left_label), Write(right_label))
        self.next_slide()

        # Add two horizontal arrows with 'Diffusion Time' text between them below the line
        diffusion_time_text = Text("Diffusion Time")
        arrow_left = Arrow(start=diffusion_time_text.get_left(), end=line.get_left(), color=WHITE)
        arrow_right = Arrow(start=diffusion_time_text.get_right(), end=line.get_right(), color=WHITE)
        diffusion_group = VGroup(arrow_left, diffusion_time_text, arrow_right).next_to(line, 4 * DOWN)
        self.play(Write(diffusion_group))
        self.next_slide()

        # Add image to the slide
        image = ImageMobject("assets/clean_image.jpg").scale(0.25)  # Scale down the image to fit better
        image.next_to(line.get_right(), 2 * UP)  # Position the image above the right end of the line
        self.play(FadeIn(image))
        self.next_slide()

        
