#!/data/data/com.termux/files/usr/bin/bash
set -e
echo "Installing IRESH AI for Termux..."
pkg update -y
pkg install -y python termux-api
mkdir -p "$HOME/.local/bin" "$HOME/iresh-ai"
cp iresh.py "$HOME/iresh-ai/iresh.py"
cat > "$HOME/.local/bin/iresh" <<'EOF'
#!/data/data/com.termux/files/usr/bin/bash
exec python "$HOME/iresh-ai/iresh.py" "$@"
EOF
chmod +x "$HOME/.local/bin/iresh"
if ! grep -q 'HOME/.local/bin' "$HOME/.bashrc" 2>/dev/null; then
  echo 'export PATH="$HOME/.local/bin:$PATH"' >> "$HOME/.bashrc"
fi
echo
echo "Installed! Run: source ~/.bashrc && iresh"
echo "Also install the Android app 'Termux:API' from the same trusted source as Termux."
