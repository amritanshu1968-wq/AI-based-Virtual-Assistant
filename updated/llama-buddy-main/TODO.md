# TODO for Integrating Text-to-Image Generation into LlamaBuddy

## Completed
- [x] Update requirements.txt with necessary dependencies (diffusers, transformers, accelerate, torch, matplotlib)

## Pending
- [x] Modify LlamaBuddy.py to integrate image generation feature
  - [x] Add imports for diffusers, torch, PIL (for images)
  - [x] Use @st.cache_resource to load Stable Diffusion pipelines
  - [x] Create a modified generate_image function that returns PIL images instead of using plt.show()
  - [x] Add a new expander in the main UI for "Image Generation"
    - [x] Text input for prompt
    - [x] Sliders/inputs for parameters (num_inference_steps, width, height, num_images, negative_prompt)
    - [x] Button to generate image
    - [x] Display generated images using st.image
  - [x] Handle errors (e.g., no CUDA, model loading issues)
- [ ] Test the integration
  - [ ] Run the app and verify image generation works
  - [ ] Ensure chat functionality remains intact
- [ ] Optional: Integrate image generation into chat (e.g., detect prompts like "generate image: ...")
