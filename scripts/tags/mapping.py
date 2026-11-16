"""Tag vocabulary and old-to-new mapping (WISH-913, plan KARAKEEP-WINDOW section 5.2).

Shared by migrate_tags.py and scripts/import-to-karakeep.py. Pure data and
one pure function, no network.
"""

from __future__ import annotations

SRC_TAG = "src-discord"

# Discord archiver source categories. Each becomes the single tag src-discord.
SOURCE_TAGS = {
    "opensourceprojects",
    "other",
    "media",
    "wrapper-only",
    "post",
    "lists",
    "opensouceprojects",
}

# Host tags: rules and the archiver add them. They stay, and are always
# attached as human so the AI retag (which deletes every AI tag first) keeps them.
HOST_TAGS = {"github", "x", "reddit", "youtube"}

# Plan section 5.2, by area. design-ui already exists (51 bookmarks).
VOCAB_BY_AREA = {
    "AI and agents": ["agents", "claude", "mcp", "skills", "llm-models", "local-ai", "prompts"],
    "Images and video": ["comfyui", "image-gen", "video-gen"],
    "Home": ["home-assistant", "homelab", "self-hosted", "hardware"],
    "Lab areas": ["media-server", "networking", "security", "backups", "monitoring", "docs-knowledge"],
    "Building": ["design-ui", "web-dev", "mobile-dev", "dev-tools", "github-repo"],
    "Other interests": ["trading", "reading"],
}
VOCAB = [t for tags in VOCAB_BY_AREA.values() for t in tags]

# Old tag name -> new tag name. A mapped tag keeps its attachedBy.
# Same-name entries in VOCAB / HOST_TAGS need no row.
TOPIC_MAP = {
    # merge
    "twitter": "x",
    # home
    "homeassistant": "home-assistant",
    "smart-home": "home-assistant",
    "matter": "home-assistant",
    "romm": "self-hosted",
    "docker": "self-hosted",
    "cnx-software": "hardware",
    # AI
    "ollama": "local-ai",
    "llmfit": "local-ai",
    "quantization": "local-ai",
    "AI": "llm-models",
    "Artificial Intelligence": "llm-models",
    "LLM": "llm-models",
    "llms": "llm-models",
    "ChatGPT": "llm-models",
    "gemini": "llm-models",
    "openai": "llm-models",
    "Grok": "llm-models",
    "perplexity": "llm-models",
    "qwen": "llm-models",
    "Andrej Karpathy": "llm-models",
    "huggingface": "llm-models",
    "agent": "agents",
    "multiagent": "agents",
    "hermes-agent": "agents",
    "aiagentskit": "agents",
    "codex": "agents",
    # images and video
    "civitai": "image-gen",
    "stable-diffusion": "image-gen",
    "lora": "image-gen",
    "diffusers": "image-gen",
    "image-to-image": "image-gen",
    # building
    "react": "web-dev",
    "shadcn": "web-dev",
    "shadcnpreset": "web-dev",
    "javascript": "web-dev",
    "webgpu": "web-dev",
    "frontend-developer": "web-dev",
    "web-design": "design-ui",
    "website-design": "design-ui",
    "ux-design": "design-ui",
    "design": "design-ui",
    "design-tools": "design-ui",
    "figma": "design-ui",
    "framer": "design-ui",
    "codepen": "design-ui",
    "tools": "dev-tools",
    "cli": "dev-tools",
    "terminal": "dev-tools",
    "Python": "dev-tools",
    "pypi": "dev-tools",
    "python-dotenv": "dev-tools",
    "libraries": "dev-tools",
    "docs": "docs-knowledge",
    "docs-repo": "docs-knowledge",
    # security
    "Security": "security",
    # trading
    "polymarket": "trading",
    "polyman": "trading",
    "getphantomflow": "trading",
    "prediction-markets": "trading",
    "crypto": "trading",
    "cryptocurrency": "trading",
    "bitcoin": "trading",
    "ethereum": "trading",
    "stocks": "trading",
    "Trading": "trading",
    "Live trading": "trading",
    "TradingView": "trading",
    "ninjatrader": "trading",
    "finance": "trading",
    "equity-curve": "trading",
    "performance-metrics": "trading",
    "win-rate": "trading",
    "profit-loss": "trading",
    "asset-performance": "trading",
    "valuation": "trading",
    "financials": "trading",
    "investment-banking": "trading",
    # reading (article sites)
    "substack": "reading",
    "medium": "reading",
    "kdnuggets": "reading",
    "infoq": "reading",
    "howtogeek": "reading",
    "thinknerd": "reading",
}

KEEP_NAMES = set(VOCAB) | HOST_TAGS | {SRC_TAG}


def target(name: str):
    """Return (new_name, rule) for an old tag name, or (None, 'unmapped')."""
    if name in SOURCE_TAGS:
        return SRC_TAG, "source"
    if name in TOPIC_MAP:
        return TOPIC_MAP[name], "map"
    if name in KEEP_NAMES:
        return name, "keep"
    return None, "unmapped"


def desired_tags(current):
    """current: list of (name, attachedBy). Returns dict name -> attachedBy.

    - source tags -> src-discord, always human (survives the AI retag)
    - mapped tags move with their attachedBy (human wins on a merge)
    - host tags are always human (survive the retag)
    - unmapped AI tags are dropped; unmapped human tags stay
    """
    out: dict[str, str] = {}

    def put(name, by):
        if out.get(name) == "human":
            return
        out[name] = by

    for name, by in current:
        new, rule = target(name)
        if rule == "source":
            put(SRC_TAG, "human")
        elif rule == "map":
            put(new, "human" if new in HOST_TAGS else by)
        elif rule == "keep":
            put(new, "human" if new in HOST_TAGS else by)
        else:  # unmapped
            if by == "human":
                put(name, "human")
    return out
