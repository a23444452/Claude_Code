# YOLO Project Development Container
# Base: Python 3.10 with CUDA support (optional)
FROM python:3.10-slim

# Build arguments
ARG TIMEZONE=Asia/Taipei
ARG CLAUDE_CODE_VERSION=latest
ARG NODE_VERSION=20

# Set environment variables
ENV DEBIAN_FRONTEND=noninteractive \
    TZ=${TIMEZONE} \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    DEVCONTAINER=true

# Install system dependencies
RUN apt-get update && apt-get install -y \
    # Basic tools
    git \
    curl \
    wget \
    vim \
    nano \
    zsh \
    sudo \
    # Network tools (for firewall script)
    iptables \
    ipset \
    dnsutils \
    # Build tools (for Python packages)
    build-essential \
    libssl-dev \
    libffi-dev \
    python3-dev \
    # Image processing libraries (for YOLO)
    libgl1-mesa-glx \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgomp1 \
    # OpenCV dependencies
    libopencv-dev \
    # Git tools
    git-lfs \
    # Timezone data
    tzdata \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Configure timezone
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# Install Node.js (required for Claude Code)
RUN curl -fsSL https://deb.nodesource.com/setup_${NODE_VERSION}.x | bash - \
    && apt-get install -y nodejs \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user
ARG USERNAME=yolo
ARG USER_UID=1000
ARG USER_GID=$USER_UID

RUN groupadd --gid $USER_GID $USERNAME \
    && useradd --uid $USER_UID --gid $USER_GID -m $USERNAME -s /bin/zsh \
    && echo "$USERNAME ALL=(ALL) NOPASSWD: /usr/local/bin/init-firewall.sh" >> /etc/sudoers.d/$USERNAME \
    && chmod 0440 /etc/sudoers.d/$USERNAME

# Create workspace directories
RUN mkdir -p /workspace \
    /home/$USERNAME/.claude \
    /home/$USERNAME/.cache/pip \
    /commandhistory \
    && chown -R $USERNAME:$USERNAME /workspace \
    /home/$USERNAME/.claude \
    /home/$USERNAME/.cache \
    /commandhistory

# Install zsh with powerline10k theme
RUN sh -c "$(wget -O- https://github.com/deluan/zsh-in-docker/releases/download/v1.2.0/zsh-in-docker.sh)" -- \
    -t robbyrussell \
    -p git \
    -p ssh-agent \
    -p https://github.com/zsh-users/zsh-autosuggestions \
    -p https://github.com/zsh-users/zsh-syntax-highlighting

# Install git-delta for better git diffs
RUN wget https://github.com/dandavison/delta/releases/download/0.18.2/git-delta_0.18.2_amd64.deb \
    && dpkg -i git-delta_0.18.2_amd64.deb \
    && rm git-delta_0.18.2_amd64.deb

# Configure git to use delta
RUN git config --global core.pager delta \
    && git config --global interactive.diffFilter "delta --color-only" \
    && git config --global delta.navigate true \
    && git config --global delta.light false \
    && git config --global delta.side-by-side true

# Install Claude Code CLI globally
RUN npm install -g @anthropic-ai/claude-code@${CLAUDE_CODE_VERSION}

# Copy firewall initialization script
COPY init-firewall.sh /usr/local/bin/init-firewall.sh
RUN chmod +x /usr/local/bin/init-firewall.sh

# Switch to non-root user
USER $USERNAME
WORKDIR /workspace

# Install Python development tools
RUN pip install --user --upgrade pip setuptools wheel

# Install Python code quality tools
RUN pip install --user \
    black \
    isort \
    flake8 \
    mypy \
    pylint \
    pytest \
    pytest-cov \
    pytest-asyncio

# Set default editor
ENV EDITOR=nano

# Configure bash history persistence
RUN echo 'export HISTFILE=/commandhistory/.bash_history' >> /home/$USERNAME/.bashrc \
    && echo 'export PROMPT_COMMAND="history -a; $PROMPT_COMMAND"' >> /home/$USERNAME/.bashrc

# Configure zsh history persistence
RUN echo 'export HISTFILE=/commandhistory/.zsh_history' >> /home/$USERNAME/.zshrc \
    && echo 'setopt SHARE_HISTORY' >> /home/$USERNAME/.zshrc

# Add helpful aliases
RUN echo 'alias ll="ls -lah"' >> /home/$USERNAME/.bashrc \
    && echo 'alias ll="ls -lah"' >> /home/$USERNAME/.zshrc \
    && echo 'alias gs="git status"' >> /home/$USERNAME/.bashrc \
    && echo 'alias gs="git status"' >> /home/$USERNAME/.zshrc

# Set Python path
ENV PATH="/home/$USERNAME/.local/bin:$PATH"

# Default command
CMD ["/bin/zsh"]
