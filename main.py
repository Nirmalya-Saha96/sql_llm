import gradio as gr
from model.llm import LlmModel
from ui.uploadFile import UploadFile


with gr.Blocks() as app:
    with gr.Tabs():
        with gr.TabItem("Q&A-and-RAG-with-SQL-and-TabularData"):
            ##############
            # First ROW:
            ##############
            with gr.Row() as row_one:
                chatbot = gr.Chatbot(
                    [],
                    elem_id="chatbot",
                    bubble_full_width=False,
                    height=500,
                    avatar_images=(
                        ("images/AI_RT.png"), "images/openai.png")
                )
            ##############
            # SECOND ROW:
            ##############
            with gr.Row():
                input_txt = gr.Textbox(
                    lines=4,
                    scale=8,
                    placeholder="Enter your prompt",
                    container=False,
                )
            ##############
            # Third ROW:
            ##############
            with gr.Row() as row_two:
                text_submit_btn = gr.Button(value="Submit")
                upload_btn = gr.UploadButton(
                    "📁 Upload CSV or XLSX files", file_types=['.csv'], file_count="multiple")
                app_functionality = gr.Dropdown(
                    label="App functionality", choices=["Chat", "Process files"], value="Chat")
                clear_button = gr.ClearButton([input_txt, chatbot])
            ##############
            # Process:
            ##############
            file_msg = upload_btn.upload(fn=UploadFile.run_pipeline, inputs=[
                upload_btn, chatbot, app_functionality], outputs=[input_txt, chatbot], queue=False)

            # txt_msg = input_txt.submit(fn=LlmModel.respond,
            #                            inputs=[chatbot, input_txt,
            #                                    "Q&A with Uploaded CSV/XLSX SQL-DB", app_functionality],
            #                            outputs=[input_txt,
            #                                     chatbot],
            #                            queue=False).then(lambda: gr.Textbox(interactive=True),
            #                                              None, [input_txt], queue=False)

            txt_msg = text_submit_btn.click(fn=LlmModel.respond,
                                            inputs=[chatbot, input_txt, app_functionality],
                                            outputs=[input_txt,
                                                     chatbot],
                                            queue=False).then(lambda: gr.Textbox(interactive=True),
                                                              None, [input_txt], queue=False)


if __name__ == "__main__":
    app.launch(share=True)
