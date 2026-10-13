#!/data/data/com.termux/files/usr/bin/bash
set -e
cd "$(dirname "$0")"
pkg update -y
pkg install -y python termux-api
mkdir -p "$HOME/.local/bin" "$HOME/iresh-ai"
cp iresh.py "$HOME/iresh-ai/iresh.py"
cat > "$HOME/.local/bin/iresh" <<'EOF'
#!/data/data/com.termux/files/usr/bin/bash
exec python "$HOME/iresh-ai/iresh.py" "$@"
EOF
chmod +x "$HOME/.local/bin/iresh"
touch "$HOME/.bashrc"
grep -q 'HOME/.local/bin' "$HOME/.bashrc" || echo 'export PATH="$HOME/.local/bin:$PATH"' >> "$HOME/.bashrc"
echo "Install complete. Run: source ~/.bashrc && iresh"
echo "Install the separate Termux:API Android app and grant microphone permission."
