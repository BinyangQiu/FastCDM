import gradio as gr
import cv2
from pathlib import Path
from fastcdm import FastCDM


CHROMEDRIVER_PATH = Path("driver/chromedriver")


def _wrap_latex(s: str) -> str:
    s = s or ""
    return s if s.strip().startswith("$$") else f"$$ {s} $$"


def preview_latex_gt(gt: str) -> str:
    return _wrap_latex(gt)


def preview_latex_pred(pred: str) -> str:
    return _wrap_latex(pred)


def compute_fastcdm(gt: str, pred: str):
    print("-" * 20)
    print("  gt:", gt)
    print("pred:", pred)
    print("-" * 20)

    driver_path = str(CHROMEDRIVER_PATH) if CHROMEDRIVER_PATH.exists() else None
    fastcdm = FastCDM(chromedriver=driver_path)
    f1, recall, precision, vis_img = fastcdm.compute(gt, pred, visualize=True)

    if vis_img is not None:
        vis_rgb = cv2.cvtColor(vis_img, cv2.COLOR_BGR2RGB)
    else:
        vis_rgb = None

    metrics_md = f"**CDM得分(F1)**: {f1:.4f}  \n**召回率**: {recall:.4f}  \n**准确率**: {precision:.4f}"
    return metrics_md, vis_rgb


with gr.Blocks(title="FastCDM 可视化") as demo:
    gr.Markdown("# FastCDM 可视化")

    with gr.Row():
        with gr.Column():
            gt_input = gr.Textbox(
                label="GT (LaTeX)",
                lines=4,
                placeholder="输入GT公式，例如: \\frac{1}{2}",
            )
            gt_md = gr.Markdown(
                value="",
                latex_delimiters=[
                    {"left": "$$", "right": "$$", "display": True},
                    {"left": "$", "right": "$", "display": False},
                    {"left": "\\(", "right": "\\)", "display": False},
                    {"left": "\\[", "right": "\\]", "display": True},
                ],
            )

            pred_input = gr.Textbox(
                label="Pred (LaTeX)",
                lines=4,
                placeholder="输入Pred公式，例如: \\frac{1}{2}",
            )
            pred_md = gr.Markdown(
                value="",
                latex_delimiters=[
                    {"left": "$$", "right": "$$", "display": True},
                    {"left": "$", "right": "$", "display": False},
                    {"left": "\\(", "right": "\\)", "display": False},
                    {"left": "\\[", "right": "\\]", "display": True},
                ],
            )

            submit_btn = gr.Button("提交并评估")

        with gr.Column():
            metrics_out = gr.Markdown(label="评估指标")
            vis_out = gr.Image(type="numpy", label="匹配可视化", format="png")

    gt_input.change(fn=preview_latex_gt, inputs=gt_input, outputs=gt_md)
    pred_input.change(fn=preview_latex_pred, inputs=pred_input, outputs=pred_md)
    submit_btn.click(
        fn=compute_fastcdm,
        inputs=[gt_input, pred_input],
        outputs=[metrics_out, vis_out],
    )


if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860)
