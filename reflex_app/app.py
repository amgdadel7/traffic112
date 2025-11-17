import reflex as rx


def index() -> rx.Component:
    return rx.center(
        rx.vstack(
            rx.heading("Traffic112 - UI", size="7"),
            rx.text("Simple Reflex front-end. Connects to your FastAPI backend."),
            rx.link("Backend docs (/docs)", href="/docs", is_external=True),
            spacing="5",
            align="center",
        ),
        min_h="100vh",
    )


app = rx.App()
app.add_page(index, route="/")



