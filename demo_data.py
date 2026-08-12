import json

INDUSTRY_DEMOS = {
    'hospital': {
        'name': 'City General Hospital',
        'icon': '🏥',
        'description': 'Experience how AI chatbots handle patient inquiries, appointments, and medical information.',
        'sample_questions': [
            "📅 Book an Appointment",
            "👨‍⚕️ Show Doctor Information",
            "📞 Get Contact Details",
            "🏥 What services do you offer?",
            "🕐 What are your visiting hours?",
            "💊 Do you have emergency services?"
        ],
        'knowledge_base': {
            'home': "City General Hospital - Your Trusted Healthcare Partner. We provide world-class medical care with state-of-the-art facilities. Our hospital is open 24/7 with emergency services available round the clock. We have 500+ beds and serve over 100,000 patients annually.",
            'about': "City General Hospital has been serving the community for over 25 years. We have 500+ beds, 200+ doctors, and state-of-the-art medical equipment. Accredited by JCI and NABH. Our team includes 150+ specialist doctors, 500+ nurses, and 800+ support staff.",
            'services': "Services offered: Cardiology, Neurology, Orthopedics, Pediatrics, Oncology, Emergency Medicine, Radiology, Pathology, Physical Therapy, Mental Health Services, Maternity Care, ICU, NICU, Day Care Surgery, Health Checkup Packages. We also offer telemedicine consultations.",
            'doctors': json.dumps({
                'doctors': [
                    {'name': 'Dr. Rajesh Kumar', 'specialty': 'Cardiology'},
                    {'name': 'Dr. Priya Sharma', 'specialty': 'Neurology'},
                    {'name': 'Dr. Amit Patel', 'specialty': 'Orthopedics'},
                    {'name': 'Dr. Sneha Reddy', 'specialty': 'Pediatrics'},
                    {'name': 'Dr. Vikram Singh', 'specialty': 'Oncology'},
                    {'name': 'Dr. Anjali Gupta', 'specialty': 'Emergency Medicine'}
                ]
            }),
            'contact': json.dumps({
                'phone': ['+91-40-1234-5678', '+91-40-1234-5679'],
                'email': ['info@citygeneralhospital.com', 'appointments@citygeneralhospital.com'],
                'address': '123 Healthcare Avenue, Medical District, Hyderabad - 500001'
            }),
            'faq': "Visiting Hours: 9 AM - 8 PM. Emergency: 24/7. Appointment Booking: Online or Phone. Insurance Accepted: Yes, all major insurance providers. Parking: Free parking available. Cafeteria: Open 7 AM - 10 PM. Pharmacy: 24/7 on-site pharmacy."
        },
        'config': {
            'contact_phone': '+91-40-1234-5678',
            'contact_email': 'info@citygeneralhospital.com',
            'contact_address': '123 Healthcare Avenue, Medical District, Hyderabad - 500001',
            'welcome_message': 'Hello! Welcome to City General Hospital. I\'m your virtual healthcare assistant. How can I help you today?',
            'theme_color': '#e74c3c'
        }
    },
    
    'education': {
        'name': 'TechVision University',
        'icon': '📚',
        'description': 'See how chatbots assist with admissions, course information, and student services.',
        'sample_questions': [
            "📝 How to Apply for Admission?",
            "📚 What courses are available?",
            "💰 Fee Structure & Scholarships",
            "📞 Contact Admissions Office",
            "👨‍🏫 How many faculty members?",
            "🎓 Placement Records"
        ],
        'knowledge_base': {
            'home': "TechVision University - Shaping Future Leaders. Ranked among top 50 universities in India. Offering UG, PG, and Doctoral programs in Engineering, Management, Sciences, and Arts.",
            'about': "Established in 2005, TechVision University has 15,000+ students, 500+ faculty members, 100+ programs across 8 schools. State-of-the-art campus with modern infrastructure. 95% placement rate with top recruiters including Google, Microsoft, and Amazon.",
            'services': "Programs: B.Tech, M.Tech, MBA, BBA, B.Sc, M.Sc, Ph.D., BA, MA, B.Com, M.Com. Specializations: AI & Machine Learning, Data Science, Robotics, Finance, Marketing, Psychology, English Literature, Economics. We also offer online courses and executive programs.",
            'doctors': json.dumps({
                'doctors': [
                    {'name': 'Prof. Suresh Kumar', 'specialty': 'Computer Science & AI'},
                    {'name': 'Prof. Meera Patel', 'specialty': 'Business Administration'},
                    {'name': 'Prof. Arjun Reddy', 'specialty': 'Data Science'},
                    {'name': 'Prof. Lakshmi Devi', 'specialty': 'Psychology & Humanities'},
                    {'name': 'Prof. Ramesh Gupta', 'specialty': 'Mechanical Engineering'},
                    {'name': 'Prof. Anita Sharma', 'specialty': 'Biotechnology'}
                ]
            }),
            'contact': json.dumps({
                'phone': ['+91-40-9876-5432', '1800-123-4567'],
                'email': ['admissions@techvision.edu', 'info@techvision.edu'],
                'address': 'Knowledge Park, HITEC City, Hyderabad - 500081'
            }),
            'faq': "Admissions: January and July intakes. Entrance Exam: TVU-CET. Scholarships: Merit-based (up to 100%) and Need-based available. Campus: 100 acres with modern hostels. Placement: 95% placement rate. Top recruiters: Google, Microsoft, Amazon, Infosys. Fee Range: ₹2-5 Lakhs per year depending on program."
        },
        'config': {
            'contact_phone': '+91-40-9876-5432',
            'contact_email': 'admissions@techvision.edu',
            'contact_address': 'Knowledge Park, HITEC City, Hyderabad - 500081',
            'welcome_message': 'Welcome to TechVision University! I can help you with admissions, courses, fees, faculty info, and more. What would you like to know?',
            'theme_color': '#3498db'
        }
    },
    
    'real_estate': {
        'name': 'DreamHome Properties',
        'icon': '🏠',
        'description': 'Explore how chatbots handle property inquiries, site visits, and buyer interactions.',
        'sample_questions': [
            "🏠 Available Properties",
            "📅 Book Site Visit",
            "💰 Price Range & EMI Options",
            "📞 Contact Sales Team",
            "📍 Project Locations",
            "📋 Property Documents Required"
        ],
        'knowledge_base': {
            'home': "DreamHome Properties - Your Dream Home Awaits. Premium residential and commercial properties across Hyderabad, Bangalore, and Mumbai. 15+ completed projects, 10,000+ happy families. RERA registered developer.",
            'about': "DreamHome Properties is a trusted real estate developer with 15 years of experience. We specialize in luxury apartments, villas, gated communities, and commercial spaces. RERA registered. Our projects have won multiple awards for design and quality.",
            'services': "Residential: 2BHK, 3BHK, 4BHK Apartments, Villas, Penthouses. Commercial: Office Spaces, Retail Shops, IT Parks. Services: Property Management, Interior Design, Home Loans, Legal Assistance, Rental Services. We also offer NRI investment options.",
            'contact': json.dumps({
                'phone': ['+91-40-5555-1234', '+91-98765-43210'],
                'email': ['sales@dreamhome.com', 'support@dreamhome.com'],
                'address': 'DreamHome Tower, Banjara Hills Road No. 12, Hyderabad - 500034'
            }),
            'faq': "Price Range: ₹50 Lakhs - ₹5 Crores. EMI Available: Yes, with all major banks. Site Visits: Mon-Sun 9AM-7PM. Loan Assistance: Available. Possession: Ready-to-move and Under Construction options. RERA Approved: Yes. Documents: PAN Card, Aadhaar, Income Proof required."
        },
        'config': {
            'contact_phone': '+91-98765-43210',
            'contact_email': 'sales@dreamhome.com',
            'contact_address': 'DreamHome Tower, Banjara Hills, Hyderabad - 500034',
            'welcome_message': 'Welcome to DreamHome Properties! Looking for your perfect home? I can help with property details, site visits, pricing, and more. How can I assist you?',
            'theme_color': '#27ae60'
        }
    },
    
    'corporate': {
        'name': 'TechSolutions Inc.',
        'icon': '🏢',
        'description': 'See how enterprise chatbots handle business inquiries, support, and client communications.',
        'sample_questions': [
            "💼 What services do you offer?",
            "🤝 Partnership Inquiries",
            "📞 Contact Sales Team",
            "💻 Technical Support",
            "📊 Case Studies",
            "🌐 Global Offices"
        ],
        'knowledge_base': {
            'home': "TechSolutions Inc. - Transforming Businesses with Technology. Leading IT services company with 5000+ employees across 10 countries. ISO 27001 certified. Fortune 500 clients trust us for digital transformation.",
            'about': "Founded in 2010, TechSolutions provides end-to-end IT services including Cloud Computing, AI/ML, Cybersecurity, Digital Transformation, and IT Consulting. We have offices in USA, UK, India, Singapore, and Australia.",
            'services': "Cloud Services (AWS, Azure, GCP), AI & Machine Learning, Cybersecurity, Digital Transformation, IT Consulting, Managed Services, Software Development, Mobile Apps, Data Analytics, Blockchain Solutions. 24/7 support available.",
            'contact': json.dumps({
                'phone': ['+1-800-TECH-HELP', '+91-40-8888-9999'],
                'email': ['business@techsolutions.com', 'support@techsolutions.com'],
                'address': 'TechSolutions Tower, Financial District, Hyderabad - 500032'
            }),
            'faq': "Support Hours: 24/7. Response Time: Under 4 hours. SLA: 99.9% uptime. Security: SOC 2 Type II certified. Certifications: ISO 27001, GDPR Compliant. Pricing: Custom quotes based on requirements. Free consultation available."
        },
        'config': {
            'contact_phone': '+1-800-TECH-HELP',
            'contact_email': 'business@techsolutions.com',
            'contact_address': 'TechSolutions Tower, Financial District, Hyderabad - 500032',
            'welcome_message': 'Hello! Welcome to TechSolutions Inc. I\'m your virtual business assistant. How can I help you explore our IT services and solutions?',
            'theme_color': '#8e44ad'
        }
    },
    
    'ecommerce': {
        'name': 'ShopSmart Online',
        'icon': '🛒',
        'description': 'Experience how e-commerce chatbots boost sales, handle orders, and support customers.',
        'sample_questions': [
            "🛍️ Today's Deals & Offers",
            "📦 Track My Order",
            "🔄 Return & Refund Policy",
            "📞 Customer Support",
            "💳 Payment Methods",
            "🚚 Delivery Information"
        ],
        'knowledge_base': {
            'home': "ShopSmart Online - India's Favorite Online Shopping Destination. 10M+ products, 50+ categories, free delivery on orders above ₹499. Easy returns within 30 days. 100M+ registered users trust us.",
            'about': "ShopSmart is one of India's largest e-commerce platforms with 100M+ registered users. We offer electronics, fashion, home appliances, books, and more at competitive prices. Founded in 2015, we deliver to 20,000+ pin codes across India.",
            'services': "Categories: Electronics, Fashion, Home & Kitchen, Books, Sports, Beauty, Toys, Groceries. Services: Same-day delivery, Easy Returns, EMI Options, Gift Cards, Express Shipping, Price Match Guarantee. We also have a premium membership program.",
            'contact': json.dumps({
                'phone': ['1800-123-4567', '1800-987-6543'],
                'email': ['help@shopsmart.com', 'orders@shopsmart.com'],
                'address': 'ShopSmart HQ, E-Commerce Park, Gachibowli, Hyderabad - 500032'
            }),
            'faq': "Free Delivery: Orders above ₹499. Returns: 30-day easy returns. Payment: COD, Cards, UPI, EMI. Delivery Time: 2-7 business days. Customer Support: 24/7 via chat, phone, email. Warranty: Manufacturer warranty on all electronics. Deals: New deals every day at 12 PM and 8 PM."
        },
        'config': {
            'contact_phone': '1800-123-4567',
            'contact_email': 'help@shopsmart.com',
            'contact_address': 'ShopSmart HQ, Gachibowli, Hyderabad - 500032',
            'welcome_message': 'Hey there! 👋 Welcome to ShopSmart Online. I can help you find great deals, track orders, check payment options, and answer any questions. What are you looking for today?',
            'theme_color': '#f39c12'
        }
    }
}
