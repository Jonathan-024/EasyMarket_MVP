# Code extrait — classes : burger-menu, menu-icon, menu-content, menu-profile, menu-profile-avatar, menu-profile-info, menu-divider, menu-link


## static\css\home.css (extrait)
```css
.menu-link,

.burger-menu {
  position: relative;
}

.burger-menu #menu-toggle {
  display: none;
}

.burger-menu .menu-icon {
  display: -webkit-box;
  display: -ms-flexbox;
  display: flex;
  -webkit-box-orient: vertical;
  -webkit-box-direction: normal;
      -ms-flex-direction: column;
          flex-direction: column;
  gap: 5px;
  cursor: pointer;
  padding: 6px;
  border-radius: 6px;
  -webkit-transition: background 0.2s;
  transition: background 0.2s;
}

.burger-menu .menu-icon:hover {
  background: #EAF6FF;
}

.burger-menu .menu-icon span {
  display: block;
  width: 22px;
  height: 4px;
  background: #0A3D62;
  border-radius: 2px;
  -webkit-transition: all 0.25s ease;
  transition: all 0.25s ease;
  -webkit-transform-origin: center;
          transform-origin: center;
}

.burger-menu {
  /* Animation burger → croix */
}

.burger-menu #menu-toggle:checked ~ .menu-icon span:nth-child(1) {
  -webkit-transform: translateY(7px) rotate(45deg);
          transform: translateY(7px) rotate(45deg);
}

.burger-menu #menu-toggle:checked ~ .menu-icon span:nth-child(2) {
  opacity: 0;
  -webkit-transform: scaleX(0);
          transform: scaleX(0);
}

.burger-menu #menu-toggle:checked ~ .menu-icon span:nth-child(3) {
  -webkit-transform: translateY(-7px) rotate(-45deg);
          transform: translateY(-7px) rotate(-45deg);
}

.burger-menu .menu-content {
  display: none;
  position: absolute;
  right: 0;
  top: calc(100% + 12px);
  background: #fff;
  border: 1px solid #D6EAFF;
  border-radius: 10px;
  padding: 12px;
  -webkit-box-shadow: 0 8px 24px rgba(30, 144, 255, 0.12);
          box-shadow: 0 8px 24px rgba(30, 144, 255, 0.12);
  -webkit-box-orient: vertical;
  -webkit-box-direction: normal;
      -ms-flex-direction: column;
          flex-direction: column;
  gap: 2px;
  min-width: 200px;
  z-index: 100;
}

.burger-menu #menu-toggle:checked ~ .menu-content {
  display: -webkit-box;
  display: -ms-flexbox;
  display: flex;
}

.burger-menu {
  /* Profil */
}

.burger-menu .menu-profile {
  display: -webkit-box;
  display: -ms-flexbox;
  display: flex;
  -webkit-box-align: center;
      -ms-flex-align: center;
          align-items: center;
  gap: 10px;
  padding: 8px 10px;
  margin-bottom: 6px;
  background: #EAF6FF;
  border-radius: 7px;
}

.burger-menu .menu-profile .menu-profile-avatar {
  width: 34px;
  height: 34px;
  background: #1E90FF;
  border-radius: 50%;
  display: -webkit-box;
  display: -ms-flexbox;
  display: flex;
  -webkit-box-align: center;
      -ms-flex-align: center;
          align-items: center;
  -webkit-box-pack: center;
      -ms-flex-pack: center;
          justify-content: center;
  color: #fff;
  font-weight: 700;
  font-size: 0.85rem;
  -ms-flex-negative: 0;
      flex-shrink: 0;
}

.burger-menu .menu-profile .menu-profile-info .name {
  font-weight: 700;
  font-size: 0.9rem;
  color: #0A3D62;
}

.burger-menu .menu-profile .menu-profile-info .status {
  font-size: 0.78rem;
  color: #5B8FB9;
}

.burger-menu {
  /* Séparateur */
}

.burger-menu .menu-divider {
  height: 1px;
  background: #D6EAFF;
  margin: 6px 0;
}

.burger-menu {
  /* Liens */
}

.burger-menu .menu-link {
  display: -webkit-box;
  display: -ms-flexbox;
  display: flex;
  -webkit-box-align: center;
      -ms-flex-align: center;
          align-items: center;
  gap: 9px;
  padding: 9px 10px;
  text-decoration: none;
  color: #2C3E50;
  font-weight: 500;
  font-size: 0.9rem;
  border-radius: 6px;
  -webkit-transition: background 0.15s, color 0.15s;
  transition: background 0.15s, color 0.15s;
}

.burger-menu .menu-link svg {
  -ms-flex-negative: 0;
      flex-shrink: 0;
  opacity: 0.7;
  -webkit-transition: opacity 0.15s;
  transition: opacity 0.15s;
}

.burger-menu .menu-link:hover {
  background: #EAF6FF;
  color: #1E90FF;
}

.burger-menu .menu-link:hover svg {
  opacity: 1;
}
```

## static\css\main.css (extrait)
```css
.burger-menu {
  position: relative;
}

.burger-menu #menu-toggle {
  display: none;
}

.burger-menu .menu-icon {
  display: -webkit-box;
  display: -ms-flexbox;
  display: flex;
  -webkit-box-orient: vertical;
  -webkit-box-direction: normal;
      -ms-flex-direction: column;
          flex-direction: column;
  gap: 5px;
  cursor: pointer;
  padding: 6px;
  border-radius: 6px;
  -webkit-transition: background 0.2s;
  transition: background 0.2s;
}

.burger-menu .menu-icon:hover {
  background: #EAF6FF;
}

.burger-menu .menu-icon span {
  display: block;
  width: 22px;
  height: 4px;
  background: #0A3D62;
  border-radius: 2px;
  -webkit-transition: all 0.25s ease;
  transition: all 0.25s ease;
  -webkit-transform-origin: center;
          transform-origin: center;
}

.burger-menu #menu-toggle:checked ~ .menu-icon span:nth-child(1) {
  -webkit-transform: translateY(7px) rotate(45deg);
          transform: translateY(7px) rotate(45deg);
}

.burger-menu #menu-toggle:checked ~ .menu-icon span:nth-child(2) {
  opacity: 0;
  -webkit-transform: scaleX(0);
          transform: scaleX(0);
}

.burger-menu #menu-toggle:checked ~ .menu-icon span:nth-child(3) {
  -webkit-transform: translateY(-7px) rotate(-45deg);
          transform: translateY(-7px) rotate(-45deg);
}

.burger-menu .menu-content {
  display: none;
  position: absolute;
  right: 0;
  top: calc(100% + 12px);
  background: #fff;
  border: 1px solid #D6EAFF;
  border-radius: 10px;
  padding: 12px;
  -webkit-box-shadow: 0 8px 24px rgba(30, 144, 255, 0.12);
          box-shadow: 0 8px 24px rgba(30, 144, 255, 0.12);
  -webkit-box-orient: vertical;
  -webkit-box-direction: normal;
      -ms-flex-direction: column;
          flex-direction: column;
  gap: 2px;
  min-width: 200px;
  z-index: 100;
}

.burger-menu #menu-toggle:checked ~ .menu-content {
  display: -webkit-box;
  display: -ms-flexbox;
  display: flex;
}
```

## static\js\main.js (extrait)
```js
const burgerMenu = document.querySelector('.burger-menu');
```

## static\scss\home.scss (extrait)
```scss
.menu-link,

.burger-menu {
  position: relative;

  #menu-toggle {
    display: none;
  }

  .menu-icon {
    display: flex;
    flex-direction: column;
    gap: 5px;
    cursor: pointer;
    padding: 6px;
    border-radius: 6px;
    transition: background 0.2s;

    &:hover {
      background: $light-blue;
    }

    span {
      display: block;
      width: 22px;
      height: 4px;
      background: $dark-blue;
      border-radius: 2px;
      transition: all 0.25s ease;
      transform-origin: center;
    }
  }

  #menu-toggle:checked ~ .menu-icon span:nth-child(1) {
    transform: translateY(7px) rotate(45deg);
  }
  #menu-toggle:checked ~ .menu-icon span:nth-child(2) {
    opacity: 0;
    transform: scaleX(0);
  }
  #menu-toggle:checked ~ .menu-icon span:nth-child(3) {
    transform: translateY(-7px) rotate(-45deg);
  }

  .menu-content {
    display: none;
    position: absolute;
    right: 0;
    top: calc(100% + 12px);
    background: #fff;
    border: 1px solid $border-blue;
    border-radius: 10px;
    padding: 12px;
    box-shadow: 0 8px 24px rgba(30, 144, 255, 0.12);
    flex-direction: column;
    gap: 2px;
    min-width: 200px;
    z-index: 100;
  }

  #menu-toggle:checked ~ .menu-content {
    display: flex;
  }

  .menu-profile {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 8px 10px;
    margin-bottom: 6px;
    background: $light-blue;
    border-radius: 7px;

    .menu-profile-avatar {
      width: 34px;
      height: 34px;
      background: $primary-blue;
      border-radius: 50%;
      display: flex;
      align-items: center;
      justify-content: center;
      color: #fff;
      font-weight: 700;
      font-size: 0.85rem;
      flex-shrink: 0;
    }

    .menu-profile-info {
      .name {
        font-weight: 700;
        font-size: 0.9rem;
        color: $dark-blue;
      }

      .status {
        font-size: 0.78rem;
        color: $muted-blue;
      }
    }
  }

  .menu-divider {
    height: 1px;
    background: $border-blue;
    margin: 6px 0;
  }

  .menu-link {
    display: flex;
    align-items: center;
    gap: 9px;
    padding: 9px 10px;
    text-decoration: none;
    color: $text-dark;
    font-weight: 500;
    font-size: 0.9rem;
    border-radius: 6px;
    transition: background 0.15s, color 0.15s;

    svg {
      flex-shrink: 0;
      opacity: 0.7;
      transition: opacity 0.15s;
    }

    &:hover {
      background: $light-blue;
      color: $primary-blue;

      svg {
        opacity: 1;
      }
    }
  }
}
```

## static\scss\main.scss (extrait)
```scss
.burger-menu {
  position: relative;

  #menu-toggle {
    display: none;
  }

  .menu-icon {
    display: flex;
    flex-direction: column;
    gap: 5px;
    cursor: pointer;
    padding: 6px;
    border-radius: 6px;
    transition: background 0.2s;

    &:hover {
      background: $light-blue;
    }

    span {
      display: block;
      width: 22px;
      height: 4px;
      background: $dark-blue;
      border-radius: 2px;
      transition: all 0.25s ease;
      transform-origin: center;
    }
  }

  #menu-toggle:checked ~ .menu-icon span:nth-child(1) {
    transform: translateY(7px) rotate(45deg);
  }
  #menu-toggle:checked ~ .menu-icon span:nth-child(2) {
    opacity: 0;
    transform: scaleX(0);
  }
  #menu-toggle:checked ~ .menu-icon span:nth-child(3) {
    transform: translateY(-7px) rotate(-45deg);
  }

  .menu-content {
    display: none;
    position: absolute;
    right: 0;
    top: calc(100% + 12px);
    background: #fff;
    border: 1px solid $border-blue;
    border-radius: 10px;
    padding: 12px;
    box-shadow: 0 8px 24px rgba(30, 144, 255, 0.12);
    flex-direction: column;
    gap: 2px;
    min-width: 200px;
    z-index: 100;
  }

  #menu-toggle:checked ~ .menu-content {
    display: flex;
  }
}
```

## templates\base.html (extrait HTML)
```html
<div class="burger-menu">
 <input id="menu-toggle" type="checkbox"/>
 <label aria-label="Menu" class="menu-icon" for="menu-toggle">
  <span>
  </span>
  <span>
  </span>
  <span>
  </span>
 </label>
 <div class="menu-content">
  {% block menu_profile %}
              {% if session.role == 'vendeur' %}
  <div class="menu-profile">
   <div class="menu-profile-avatar">
    {{ session.vendeur_initiales }}
   </div>
   <div class="menu-profile-info">
    <p class="name">
     {{ session.vendeur_nom }}
    </p>
    <p class="status">
     Vendeur
    </p>
   </div>
  </div>
  <div class="menu-divider">
  </div>
  {% elif session.role == 'admin' %}
  <div class="menu-profile">
   <div class="menu-profile-avatar">
    AD
   </div>
   <div class="menu-profile-info">
    <p class="name">
     Administrateur
    </p>
    <p class="status">
     Admin
    </p>
   </div>
  </div>
  <div class="menu-divider">
  </div>
  {% endif %}
              {% endblock %}
  <a class="menu-link" href="{{ url_for('main.home') }}">
   <svg aria-hidden="true" fill="none" height="16" stroke="#1E90FF" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" viewbox="0 0 24 24" width="16">
    <path d="M3 9l9-7 9 7v11a2 2 0 01-2 2H5a2 2 0 01-2-2z">
    </path>
    <polyline points="9 22 9 12 15 12 15 22">
    </polyline>
   </svg>
   Accueil
  </a>
  {% if session.role == 'vendeur' %}
  <a class="menu-link" href="{{ url_for('vendeur.boutique') }}">
   <svg aria-hidden="true" fill="none" height="16" stroke="#1E90FF" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" viewbox="0 0 24 24" width="16">
    <path d="M3 9h18v10a2 2 0 01-2 2H5a2 2 0 01-2-2V9z">
    </path>
    <path d="M3 9l2.5-5h13L21 9">
    </path>
    <line x1="12" x2="12" y1="9" y2="21">
    </line>
   </svg>
   Boutique
  </a>
  <a class="menu-link" href="{{ url_for('vendeur.reservation') }}">
   <svg aria-hidden="true" fill="none" height="16" stroke="#1E90FF" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" viewbox="0 0 24 24" width="16">
    <rect height="18" rx="2" width="18" x="3" y="4">
    </rect>
    <line x1="16" x2="16" y1="2" y2="6">
    </line>
    <line x1="8" x2="8" y1="2" y2="6">
    </line>
    <line x1="3" x2="21" y1="10" y2="10">
    </line>
   </svg>
   Réservation
  </a>
  <a class="menu-link" href="{{ url_for('vendeur.dashboard') }}">
   <svg aria-hidden="true" fill="none" height="16" stroke="#1E90FF" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" viewbox="0 0 24 24" width="16">
    <rect height="7" width="7" x="3" y="3">
    </rect>
    <rect height="7" width="7" x="14" y="3">
    </rect>
    <rect height="7" width="7" x="3" y="14">
    </rect>
    <rect height="7" width="7" x="14" y="14">
    </rect>
   </svg>
   Tableau de bord
  </a>
  {% endif %}

              {% if session.role == 'admin' %}
  <a class="menu-link" href="{{ url_for('admin.dashboard') }}">
   <svg aria-hidden="true" fill="none" height="16" stroke="#1E90FF" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" viewbox="0 0 24 24" width="16">
    <rect height="7" width="7" x="3" y="3">
    </rect>
    <rect height="7" width="7" x="14" y="3">
    </rect>
    <rect height="7" width="7" x="3" y="14">
    </rect>
    <rect height="7" width="7" x="14" y="14">
    </rect>
   </svg>
   Administration
  </a>
  {% endif %}
  <a class="menu-link" href="{{ url_for('main.home') }}#about">
   <svg aria-hidden="true" fill="none" height="16" stroke="#1E90FF" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" viewbox="0 0 24 24" width="16">
    <circle cx="12" cy="12" r="10">
    </circle>
    <line x1="12" x2="12" y1="8" y2="12">
    </line>
    <line x1="12" x2="12.01" y1="16" y2="16">
    </line>
   </svg>
   À propos
  </a>
  <a class="menu-link" href="{{ url_for('main.home') }}#contact">
   <svg aria-hidden="true" fill="none" height="16" stroke="#1E90FF" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" viewbox="0 0 24 24" width="16">
    <circle cx="12" cy="12" r="10">
    </circle>
    <path d="M9.09 9a3 3 0 015.83 1c0 2-3 3-3 3">
    </path>
    <line x1="12" x2="12.01" y1="17" y2="17">
    </line>
   </svg>
   Aide
  </a>
  {% block menu_extra_links %}{% endblock %}
  <div class="menu-divider">
  </div>
  {% block menu_logout %}
              {% if session.role %}
  <form action="{{ url_for('auth.logout') }}" method="post" style="margin:0;">
   <button class="btn danger" type="submit">
    Déconnexion
   </button>
  </form>
  {% endif %}
              {% endblock %}
 </div>
</div>


<label aria-label="Menu" class="menu-icon" for="menu-toggle">
 <span>
 </span>
 <span>
 </span>
 <span>
 </span>
</label>


<div class="menu-content">
 {% block menu_profile %}
              {% if session.role == 'vendeur' %}
 <div class="menu-profile">
  <div class="menu-profile-avatar">
   {{ session.vendeur_initiales }}
  </div>
  <div class="menu-profile-info">
   <p class="name">
    {{ session.vendeur_nom }}
   </p>
   <p class="status">
    Vendeur
   </p>
  </div>
 </div>
 <div class="menu-divider">
 </div>
 {% elif session.role == 'admin' %}
 <div class="menu-profile">
  <div class="menu-profile-avatar">
   AD
  </div>
  <div class="menu-profile-info">
   <p class="name">
    Administrateur
   </p>
   <p class="status">
    Admin
   </p>
  </div>
 </div>
 <div class="menu-divider">
 </div>
 {% endif %}
              {% endblock %}
 <a class="menu-link" href="{{ url_for('main.home') }}">
  <svg aria-hidden="true" fill="none" height="16" stroke="#1E90FF" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" viewbox="0 0 24 24" width="16">
   <path d="M3 9l9-7 9 7v11a2 2 0 01-2 2H5a2 2 0 01-2-2z">
   </path>
   <polyline points="9 22 9 12 15 12 15 22">
   </polyline>
  </svg>
  Accueil
 </a>
 {% if session.role == 'vendeur' %}
 <a class="menu-link" href="{{ url_for('vendeur.boutique') }}">
  <svg aria-hidden="true" fill="none" height="16" stroke="#1E90FF" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" viewbox="0 0 24 24" width="16">
   <path d="M3 9h18v10a2 2 0 01-2 2H5a2 2 0 01-2-2V9z">
   </path>
   <path d="M3 9l2.5-5h13L21 9">
   </path>
   <line x1="12" x2="12" y1="9" y2="21">
   </line>
  </svg>
  Boutique
 </a>
 <a class="menu-link" href="{{ url_for('vendeur.reservation') }}">
  <svg aria-hidden="true" fill="none" height="16" stroke="#1E90FF" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" viewbox="0 0 24 24" width="16">
   <rect height="18" rx="2" width="18" x="3" y="4">
   </rect>
   <line x1="16" x2="16" y1="2" y2="6">
   </line>
   <line x1="8" x2="8" y1="2" y2="6">
   </line>
   <line x1="3" x2="21" y1="10" y2="10">
   </line>
  </svg>
  Réservation
 </a>
 <a class="menu-link" href="{{ url_for('vendeur.dashboard') }}">
  <svg aria-hidden="true" fill="none" height="16" stroke="#1E90FF" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" viewbox="0 0 24 24" width="16">
   <rect height="7" width="7" x="3" y="3">
   </rect>
   <rect height="7" width="7" x="14" y="3">
   </rect>
   <rect height="7" width="7" x="3" y="14">
   </rect>
   <rect height="7" width="7" x="14" y="14">
   </rect>
  </svg>
  Tableau de bord
 </a>
 {% endif %}

              {% if session.role == 'admin' %}
 <a class="menu-link" href="{{ url_for('admin.dashboard') }}">
  <svg aria-hidden="true" fill="none" height="16" stroke="#1E90FF" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" viewbox="0 0 24 24" width="16">
   <rect height="7" width="7" x="3" y="3">
   </rect>
   <rect height="7" width="7" x="14" y="3">
   </rect>
   <rect height="7" width="7" x="3" y="14">
   </rect>
   <rect height="7" width="7" x="14" y="14">
   </rect>
  </svg>
  Administration
 </a>
 {% endif %}
 <a class="menu-link" href="{{ url_for('main.home') }}#about">
  <svg aria-hidden="true" fill="none" height="16" stroke="#1E90FF" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" viewbox="0 0 24 24" width="16">
   <circle cx="12" cy="12" r="10">
   </circle>
   <line x1="12" x2="12" y1="8" y2="12">
   </line>
   <line x1="12" x2="12.01" y1="16" y2="16">
   </line>
  </svg>
  À propos
 </a>
 <a class="menu-link" href="{{ url_for('main.home') }}#contact">
  <svg aria-hidden="true" fill="none" height="16" stroke="#1E90FF" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" viewbox="0 0 24 24" width="16">
   <circle cx="12" cy="12" r="10">
   </circle>
   <path d="M9.09 9a3 3 0 015.83 1c0 2-3 3-3 3">
   </path>
   <line x1="12" x2="12.01" y1="17" y2="17">
   </line>
  </svg>
  Aide
 </a>
 {% block menu_extra_links %}{% endblock %}
 <div class="menu-divider">
 </div>
 {% block menu_logout %}
              {% if session.role %}
 <form action="{{ url_for('auth.logout') }}" method="post" style="margin:0;">
  <button class="btn danger" type="submit">
   Déconnexion
  </button>
 </form>
 {% endif %}
              {% endblock %}
</div>


<div class="menu-profile">
 <div class="menu-profile-avatar">
  {{ session.vendeur_initiales }}
 </div>
 <div class="menu-profile-info">
  <p class="name">
   {{ session.vendeur_nom }}
  </p>
  <p class="status">
   Vendeur
  </p>
 </div>
</div>


<div class="menu-profile-avatar">
 {{ session.vendeur_initiales }}
</div>


<div class="menu-profile-info">
 <p class="name">
  {{ session.vendeur_nom }}
 </p>
 <p class="status">
  Vendeur
 </p>
</div>


<div class="menu-profile">
 <div class="menu-profile-avatar">
  AD
 </div>
 <div class="menu-profile-info">
  <p class="name">
   Administrateur
  </p>
  <p class="status">
   Admin
  </p>
 </div>
</div>


<div class="menu-profile-avatar">
 AD
</div>


<div class="menu-profile-info">
 <p class="name">
  Administrateur
 </p>
 <p class="status">
  Admin
 </p>
</div>


<div class="menu-profile-avatar">
 {{ session.vendeur_initiales }}
</div>


<div class="menu-profile-avatar">
 AD
</div>


<div class="menu-profile-info">
 <p class="name">
  {{ session.vendeur_nom }}
 </p>
 <p class="status">
  Vendeur
 </p>
</div>


<div class="menu-profile-info">
 <p class="name">
  Administrateur
 </p>
 <p class="status">
  Admin
 </p>
</div>


<div class="menu-divider">
</div>


<div class="menu-divider">
</div>


<div class="menu-divider">
</div>


<a class="menu-link" href="{{ url_for('main.home') }}">
 <svg aria-hidden="true" fill="none" height="16" stroke="#1E90FF" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" viewbox="0 0 24 24" width="16">
  <path d="M3 9l9-7 9 7v11a2 2 0 01-2 2H5a2 2 0 01-2-2z">
  </path>
  <polyline points="9 22 9 12 15 12 15 22">
  </polyline>
 </svg>
 Accueil
</a>


<a class="menu-link" href="{{ url_for('vendeur.boutique') }}">
 <svg aria-hidden="true" fill="none" height="16" stroke="#1E90FF" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" viewbox="0 0 24 24" width="16">
  <path d="M3 9h18v10a2 2 0 01-2 2H5a2 2 0 01-2-2V9z">
  </path>
  <path d="M3 9l2.5-5h13L21 9">
  </path>
  <line x1="12" x2="12" y1="9" y2="21">
  </line>
 </svg>
 Boutique
</a>


<a class="menu-link" href="{{ url_for('vendeur.reservation') }}">
 <svg aria-hidden="true" fill="none" height="16" stroke="#1E90FF" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" viewbox="0 0 24 24" width="16">
  <rect height="18" rx="2" width="18" x="3" y="4">
  </rect>
  <line x1="16" x2="16" y1="2" y2="6">
  </line>
  <line x1="8" x2="8" y1="2" y2="6">
  </line>
  <line x1="3" x2="21" y1="10" y2="10">
  </line>
 </svg>
 Réservation
</a>


<a class="menu-link" href="{{ url_for('vendeur.dashboard') }}">
 <svg aria-hidden="true" fill="none" height="16" stroke="#1E90FF" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" viewbox="0 0 24 24" width="16">
  <rect height="7" width="7" x="3" y="3">
  </rect>
  <rect height="7" width="7" x="14" y="3">
  </rect>
  <rect height="7" width="7" x="3" y="14">
  </rect>
  <rect height="7" width="7" x="14" y="14">
  </rect>
 </svg>
 Tableau de bord
</a>


<a class="menu-link" href="{{ url_for('admin.dashboard') }}">
 <svg aria-hidden="true" fill="none" height="16" stroke="#1E90FF" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" viewbox="0 0 24 24" width="16">
  <rect height="7" width="7" x="3" y="3">
  </rect>
  <rect height="7" width="7" x="14" y="3">
  </rect>
  <rect height="7" width="7" x="3" y="14">
  </rect>
  <rect height="7" width="7" x="14" y="14">
  </rect>
 </svg>
 Administration
</a>


<a class="menu-link" href="{{ url_for('main.home') }}#about">
 <svg aria-hidden="true" fill="none" height="16" stroke="#1E90FF" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" viewbox="0 0 24 24" width="16">
  <circle cx="12" cy="12" r="10">
  </circle>
  <line x1="12" x2="12" y1="8" y2="12">
  </line>
  <line x1="12" x2="12.01" y1="16" y2="16">
  </line>
 </svg>
 À propos
</a>


<a class="menu-link" href="{{ url_for('main.home') }}#contact">
 <svg aria-hidden="true" fill="none" height="16" stroke="#1E90FF" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" viewbox="0 0 24 24" width="16">
  <circle cx="12" cy="12" r="10">
  </circle>
  <path d="M9.09 9a3 3 0 015.83 1c0 2-3 3-3 3">
  </path>
  <line x1="12" x2="12.01" y1="17" y2="17">
  </line>
 </svg>
 Aide
</a>

```