const terminalText = document.getElementById('terminal-text');
const terminalOutput = document.getElementById('terminal-output');

const commands = [
  { text: "pallas start", output: "Initializing Pallas Core... [OK]\nLoading Memory (FTS5)... [OK]\nWelcome, Operator." },
  { text: "pallas ask 'Research AI Agent autonomy'", output: "Searching web... [DuckDuckGo]\nExtracting content... [arXiv]\nSynthesis in progress..." },
  { text: "pallas doctor", output: "Diagnostics: All APIs responsive. Environment: Healthy." }
];

let cmdIndex = 0;

async function typeCommand() {
  const cmd = commands[cmdIndex];
  terminalText.textContent = "";
  terminalOutput.textContent = "";
  
  for (let i = 0; i < cmd.text.length; i++) {
    terminalText.textContent += cmd.text[i];
    await new Promise(r => setTimeout(r, 100));
  }
  
  await new Promise(r => setTimeout(r, 500));
  terminalOutput.textContent = cmd.output;
  
  await new Promise(r => setTimeout(r, 3000));
  cmdIndex = (cmdIndex + 1) % commands.length;
  typeCommand();
}

document.addEventListener('DOMContentLoaded', () => {
  typeCommand();
  
  // Simple scroll reveal for glass cards
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.style.opacity = '1';
        entry.target.style.transform = 'translateY(0)';
      }
    });
  }, { threshold: 0.1 });

  document.querySelectorAll('.glass-card').forEach(card => {
    card.style.opacity = '0';
    card.style.transform = 'translateY(20px)';
    card.style.transition = 'all 0.6s cubic-bezier(0.22, 1, 0.36, 1)';
    observer.observe(card);
  });
});
