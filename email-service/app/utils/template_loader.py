from jinja2 import Environment, FileSystemLoader
import os


template_dir = os.path.join(os.path.dirname(__file__), '..', 'templates')
env = Environment(loader=FileSystemLoader(template_dir))


def load_template(template_name: str, context: dict) -> str:
    """Loads and renders an HTML email template.

    Args:
        template_name (str): Template file name.
        context (dict): Data context for rendering the template.

    Returns:
        str: Rendered HTML content.
    """
    template = env.get_template(template_name)
    return template.render(context)
