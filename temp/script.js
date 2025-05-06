const userData = {
    first_name: "John",
    last_name: "Doe",
    email: "john.doe@example.com",
    image: "https://images.unsplash.com/photo-1581092795360-fd1ca04f0952",
    addresses: { count: "2" },
    referrals: { count: "5" },
    payment_methods: { count: "3" },
    unread_notifications: { count: "4" }
  };
  
  // Profile options data
  const profileOptions = [
    {
      id: 'address',
      title: 'Manage Addresses',
      icon: '<i class="fas fa-map-marker-alt"></i>',
      iconColor: 'var(--primary)',
      description: 'Add, edit or remove delivery addresses',
      linkText: 'Manage',
      count: userData.addresses.count
    },
    {
      id: 'referral',
      title: 'Referrals',
      icon: '<i class="fas fa-users"></i>',
      iconColor: 'var(--secondary)',
      description: 'Invite friends & earn rewards',
      linkText: 'Invite',
      count: userData.referrals.count
    },
    {
      id: 'payment',
      title: 'Payment Methods',
      icon: '<i class="fas fa-credit-card"></i>',
      iconColor: 'var(--accent)',
      description: 'Add or remove payment methods',
      linkText: 'Manage',
      count: userData.payment_methods.count
    },
    {
      id: 'notifications',
      title: 'Notifications',
      icon: '<i class="fas fa-bell"></i>',
      iconColor: 'var(--primary)',
      description: 'Manage email & push notifications',
      linkText: 'Settings',
      badge: userData.unread_notifications.count
    },
    {
      id: 'privacy',
      title: 'Privacy & Security',
      icon: '<i class="fas fa-lock"></i>',
      iconColor: 'var(--secondary)',
      description: 'Manage your account security',
      linkText: 'Update',
    },
    {
      id: 'support',
      title: 'Contact Support',
      icon: '<i class="fas fa-phone"></i>',
      iconColor: 'var(--accent)',
      description: 'Get help with your orders',
      linkText: 'Contact',
    }
  ];
  
  // Food emoji array for promo banner
  const foodEmojis = ['🍕', '🍔', '🍜', '🍣', '🥗', '🍦', '🌮'];
  
  // DOM elements
  const profileToggle = document.getElementById('profileToggle');
  const closeSidebar = document.getElementById('closeSidebar');
  const userSidebar = document.getElementById('userSidebar');
  const overlay = document.getElementById('overlay');
  const profileOptionsGrid = document.querySelector('.profile-options-grid');
  const foodIcons = document.querySelector('.food-icons');
  const currentYearEl = document.getElementById('currentYear');
  const bannerHeading = document.querySelector('.banner-content h2');
  const userProfile = document.querySelector('.user-profile');
  
  // Update user information
  document.addEventListener('DOMContentLoaded', () => {
    // Update welcome message with user's name
    bannerHeading.textContent = `Welcome back, ${userData.first_name}!`;
    
    // Set current year in footer
    currentYearEl.textContent = new Date().getFullYear();
    
    // Generate food icons for promo banner
    generateFoodIcons();
    
    // Render profile options
    renderProfileOptions();
  });
  
  // Toggle sidebar
  profileToggle.addEventListener('click', () => {
    userSidebar.classList.add('active');
    overlay.classList.add('active');
    userProfile.classList.add('shift-left');
  });
  
  // Close sidebar
  closeSidebar.addEventListener('click', () => {
    userSidebar.classList.remove('active');
    overlay.classList.remove('active');
    userProfile.classList.remove('shift-left');
  });
  
  // Close sidebar when clicking overlay
  overlay.addEventListener('click', () => {
    userSidebar.classList.remove('active');
    overlay.classList.remove('active');
    userProfile.classList.remove('shift-left');
  });
  
  // Generate food icons for promo banner
  function generateFoodIcons() {
    for (let i = 0; i < 20; i++) {
      const foodIcon = document.createElement('div');
      foodIcon.className = 'food-icon';
      foodIcon.textContent = foodEmojis[Math.floor(Math.random() * foodEmojis.length)];
      
      // Random positioning
      const top = Math.random() * 100;
      const left = Math.random() * 100;
      const rotation = Math.random() * 360;
      
      foodIcon.style.top = `${top}%`;
      foodIcon.style.left = `${left}%`;
      foodIcon.style.transform = `rotate(${rotation}deg)`;
      
      foodIcons.appendChild(foodIcon);
    }
  }
  
  // Render profile options
  function renderProfileOptions() {
    profileOptionsGrid.innerHTML = '';
    
    profileOptions.forEach(option => {
      const optionElement = document.createElement('div');
      optionElement.className = 'profile-option';
      optionElement.id = `option-${option.id}`;
      
      const headerContent = `
        <div class="option-header">
          <div class="option-icon" style="color: ${option.iconColor}">
            ${option.icon}
          </div>
          ${option.count ? `<span class="option-count">${option.count} ${parseInt(option.count) === 1 ? 'item' : 'items'}</span>` : ''}
          ${option.badge ? `<span class="option-badge">${option.badge}</span>` : ''}
        </div>
      `;
      
      const optionContent = `
        <h3 class="option-title">${option.title}</h3>
        <p class="option-description">${option.description}</p>
        <a href="#" class="option-link">${option.linkText} →</a>
      `;
      
      optionElement.innerHTML = headerContent + optionContent;
      profileOptionsGrid.appendChild(optionElement);
    });
  }