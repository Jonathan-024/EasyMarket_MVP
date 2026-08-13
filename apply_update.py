import os

# --- CONFIGURATION DES TÂCHES ---
TASKS = [
    {
        "file": "templates/base.html",
        "action": "replace_block",
        "start_marker": "<!-- FOOTER -->",
        "end_marker": "</footer>",
        "content": """<!-- FOOTER -->
  <footer>
    <div class="footer-content">
      <div class="footer-top">
        <div class="footer-brand">
          <span class="brand-name">
            <span class="brand-easy">Easy</span><span class="brand-market">Market |</span>
            <span class="footer-tagline">Le marché facile — pour tous !</span>
          </span>
        </div>
        <div class="footer-links">
          <a href="https://wa.me/VOTRE_NUMERO" class="footer-link" target="_blank" rel="noopener noreferrer" aria-label="WhatsApp">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="#25D366" aria-hidden="true"><path d="M20.52 3.48A11.93 11.93 0 0012 0C5.37 0 0 5.37 0 12c0 2.11.55 4.16 1.6 5.97L0 24l6.18-1.57A11.94 11.94 0 0012 24c6.63 0 12-5.37 12-12 0-3.2-1.25-6.21-3.48-8.52zM12 22c-1.85 0-3.66-.5-5.23-1.43l-.37-.22-3.87.98.99-3.76-.24-.38A9.94 9.94 0 012 12C2 6.48 6.48 2 12 2c2.67 0 5.18 1.04 7.07 2.93A9.94 9.94 0 0122 12c0 5.52-4.48 10-10 10zm5.44-7.3c-.3-.15-1.76-.87-2.03-.97-.27-.1-.47-.15-.67.15-.2.3-.77.97-.94 1.17-.17.2-.35.22-.65.07-.3-.15-1.27-.47-2.42-1.5-.9-.8-1.5-1.79-1.68-2.09-.17-.3-.02-.46.13-.61.13-.13.3-.35.45-.52.15-.17.2-.3.3-.5.1-.2.05-.37-.02-.52-.07-.15-.67-1.6-.91-2.2-.24-.58-.48-.5-.67-.51H6.9c-.2 0-.52.07-.79.37C5.84 8.2 5.1 8.9 5.1 10.35s1.05 2.87 1.2 3.07c.15.2 2.07 3.16 5.01 4.43.7.3 1.25.48 1.67.62.7.22 1.34.19 1.84.12.56-.08 1.76-.72 2.01-1.41.25-.7.25-1.29.17-1.41-.07-.13-.27-.2-.57-.35z"/></svg>
          </a>
        </div>
      </div>
      <div class="footer-bottom">
        <p>&copy; 2026 EasyMarket. Tous droits réservés.</p>
        <a href="#" class="footer-link legal-link">Mentions légales</a>
      </div>
    </div>
  </footer>"""
    },
    {
        "file": "static/scss/main.scss",
        "action": "append",
        "content": """

/* ─── Footer ────────────────────────────────────────────── */
footer {
  background: #0A3D62;
  color: #fff;
  padding: 30px 20px 24px;

  .footer-content {
    max-width: 800px;
    margin: 0 auto;
    display: flex;
    flex-direction: column;
    gap: 20px;

    .footer-top {
      display: flex;
      justify-content: space-between;
      align-items: center;

      .footer-brand {
        display: flex;
        flex-direction: column;
        gap: 6px;

        .brand-name {
          font-size: 1.3rem;
          font-weight: 800;
          letter-spacing: -0.3px;

          .brand-easy {
            color: #4EABFF;
          }
          .brand-market {
            color: #fff;
          }
        }

        .footer-tagline {
          font-size: 1rem;
          font-weight: 200;
          color: rgba(255, 255, 255, 0.45);
        }
      }
    }

    .footer-links {
      display: flex;
      align-items: center;
      gap: 10px;

      .footer-link {
        display: flex;
        align-items: center;
        gap: 7px;
        text-decoration: none;
        font-size: 0.7rem;
        font-weight: 500;
        color: rgba(255, 255, 255, 0.7);
        transition: color 0.2s ease;
        &:hover {
          color: #fff;
        }
      }
    }
    
    .footer-bottom {
      padding-top: 16px;
      border-top: 1px solid rgba(255, 255, 255, 0.1);
      text-align: center;

      p {
        font-size: 0.8rem;
        color: rgba(255, 255, 255, 0.3);
      }
    }

    .legal-link {
      display: inline-block;
      margin-top: 10px;
      text-decoration: none;
      font-size: 0.85rem;
      color: darken($primary-blue, 10%);
      &:hover {
        color: $primary-blue;
        text-decoration: underline;
      }
    }
  }
}"""
    }
]

def apply_updates():
    for task in TASKS:
        try:
            if not os.path.exists(task['file']):
                print(f"⚠️ Fichier introuvable : {task['file']}")
                continue

            with open(task['file'], 'r', encoding='utf-8') as f:
                content = f.read()

            if task['action'] == 'replace_block':
                start = content.find(task['start_marker'])
                end = content.find(task['end_marker'], start) + len(task['end_marker'])
                if start != -1 and end != -1:
                    new_content = content[:start] + task['content'] + content[end:]
                    with open(task['file'], 'w', encoding='utf-8') as f:
                        f.write(new_content)
                else:
                    print(f"❌ Marqueurs non trouvés dans {task['file']}")
                    continue
            
            elif task['action'] == 'append':
                with open(task['file'], 'a', encoding='utf-8') as f:
                    f.write(task['content'])
            
            print(f"✅ Succès : {task['file']} mis à jour.")
        except Exception as e:
            print(f"❌ Erreur sur {task['file']} : {e}")

if __name__ == "__main__":
    apply_updates()