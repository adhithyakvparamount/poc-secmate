"""Session-backed workspace preferences and lightweight localization."""

import streamlit as st


LANGUAGES = ["English", "Hindi", "Arabic", "French"]
ENVIRONMENTS = ["Staging", "Production", "Local"]
DENSITIES = ["Comfortable", "Compact", "Spacious"]
USER_TYPES = ["Student", "Engineer", "Working Professional", "Security Analyst", "Founder / Product Owner", "Other"]
USE_CASES = [
    "Learning AI security",
    "Testing an internal AI agent",
    "Client security assessments",
    "Compliance and audit reports",
    "Research and experimentation",
    "Production monitoring",
]


TEXT = {
    "English": {
        "profile": "Profile",
        "settings": "Settings",
        "plan": "Plan",
        "account_type": "Account type",
        "name": "Name",
        "language": "Language",
        "environment": "Environment",
        "dashboard_density": "Dashboard density",
        "reduced_motion": "Reduced motion",
        "notifications": "Notifications",
        "no_notifications": "No notifications yet.",
        "mark_all_read": "Mark all read",
        "clear": "Clear",
        "new": "New",
        "notification_ready_title": "Notification center ready",
        "notification_ready_message": "Assessment completions and new findings will appear here.",
        "loading_title": "Preparing your SecMate workspace",
        "loading_subtitle": "Loading onboarding, profile, and assessment defaults.",
        "onboarding_kicker": "SECURITY WORKSPACE SETUP",
        "onboarding_title": "Set up your first AI security assessment.",
        "onboarding_copy": "Connect a target, select security coverage, review findings, and export an assessment report.",
        "step_connect": "Connect your target",
        "step_connect_desc": "Add the AI agent endpoint and the authentication method SecMate should use.",
        "step_coverage": "Pick security coverage",
        "step_coverage_desc": "Choose Red Team, Blue Team, and VAPT checks for your first run.",
        "step_findings": "Review live findings",
        "step_findings_desc": "Track severity, evidence, and guardrail behavior in one view.",
        "step_report": "Export the report",
        "step_report_desc": "Generate a stakeholder-ready report after validation is complete.",
        "about_use_case": "Tell us about your use case",
        "user_type_question": "Which best describes you?",
        "use_case_question": "What will you use SecMate for?",
        "goal_question": "Anything specific you want SecMate to help with?",
        "goal_placeholder": "Example: test prompt injection risks before deploying a support bot.",
        "workspace_preferences": "Workspace preferences",
        "enter_dashboard": "Enter Dashboard",
        "preferences_hint": "These choices are saved for this signed-in workspace and can be changed later.",
        "dashboard": "Dashboard",
        "workspace": "workspace",
        "optimized_for": "Optimized for",
        "new_assessment": "New Assessment",
        "workspace_health": "Workspace health",
        "ready": "ready",
        "unread_notifications": "{count} unread notifications",
        "settings_subtitle": "Manage workspace appearance, language, environment, and assessment defaults.",
        "appearance": "Appearance",
        "theme": "Theme",
        "save_settings": "Save Settings",
        "settings_saved": "Workspace settings saved and applied.",
        "new_assessment_subtitle": "Configure a target and launch a Red Team, Blue Team, or full VAPT run.",
        "results_title": "Red Team & Blue Team Results",
        "results_subtitle": "Adversarial prompts and target evaluations for the selected run.",
        "findings_title": "VAPT Findings",
        "findings_subtitle": "Rule-based evidence analysis across completed assessments.",
        "reports": "Reports",
        "reports_subtitle": "Generate and download assessment reports for stakeholders and audit trails.",
        "integrations": "Integrations",
        "integrations_subtitle": "Connect SecMate with issue trackers, SIEM, cloud, and reporting workflows.",
        "profile_subtitle": "Manage your SecMate identity, workspace role, and recent account activity.",
    },
    "Hindi": {
        "profile": "प्रोफ़ाइल", "settings": "सेटिंग्स", "plan": "योजना", "account_type": "खाता प्रकार",
        "name": "नाम", "language": "भाषा", "environment": "परिवेश", "dashboard_density": "डैशबोर्ड घनत्व",
        "reduced_motion": "कम एनीमेशन", "notifications": "सूचनाएं", "no_notifications": "अभी कोई सूचना नहीं है।",
        "mark_all_read": "सभी को पढ़ा मानें", "clear": "साफ़ करें", "new": "नया",
        "notification_ready_title": "सूचना केंद्र तैयार है", "notification_ready_message": "आकलन और नई खोजें यहां दिखाई देंगी।",
        "loading_title": "आपका SecMate कार्यक्षेत्र तैयार हो रहा है", "loading_subtitle": "ऑनबोर्डिंग और प्राथमिकताएं लोड हो रही हैं।",
        "onboarding_kicker": "सुरक्षा कार्यक्षेत्र सेटअप", "onboarding_title": "अपना पहला AI सुरक्षा आकलन सेट करें।",
        "onboarding_copy": "लक्ष्य जोड़ें, सुरक्षा कवरेज चुनें, निष्कर्ष देखें और रिपोर्ट निर्यात करें।",
        "step_connect": "लक्ष्य जोड़ें", "step_connect_desc": "AI एजेंट एंडपॉइंट और प्रमाणीकरण विधि जोड़ें।",
        "step_coverage": "सुरक्षा कवरेज चुनें", "step_coverage_desc": "Red Team, Blue Team और VAPT जांच चुनें।",
        "step_findings": "लाइव निष्कर्ष देखें", "step_findings_desc": "गंभीरता, प्रमाण और गार्डरेल व्यवहार देखें।",
        "step_report": "रिपोर्ट निर्यात करें", "step_report_desc": "सत्यापन के बाद हितधारक रिपोर्ट बनाएं।",
        "about_use_case": "अपने उपयोग के बारे में बताएं", "user_type_question": "आपका सबसे अच्छा वर्णन क्या है?",
        "use_case_question": "आप SecMate का उपयोग किस लिए करेंगे?", "goal_question": "SecMate से कोई विशेष सहायता चाहिए?",
        "goal_placeholder": "उदाहरण: सपोर्ट बॉट तैनात करने से पहले प्रॉम्प्ट इंजेक्शन जांचें।",
        "workspace_preferences": "कार्यक्षेत्र प्राथमिकताएं", "enter_dashboard": "डैशबोर्ड खोलें",
        "preferences_hint": "ये विकल्प इस कार्यक्षेत्र के लिए सहेजे जाते हैं और बाद में बदले जा सकते हैं।",
        "dashboard": "डैशबोर्ड", "workspace": "कार्यक्षेत्र", "optimized_for": "इसके लिए अनुकूलित",
        "new_assessment": "नया आकलन", "workspace_health": "कार्यक्षेत्र स्थिति", "ready": "तैयार",
        "unread_notifications": "{count} अपठित सूचनाएं", "settings_subtitle": "भाषा, परिवेश और रूप बदलें।",
        "appearance": "रूप", "theme": "थीम", "save_settings": "सेटिंग्स सहेजें", "settings_saved": "कार्यक्षेत्र सेटिंग्स लागू हो गईं।",
        "new_assessment_subtitle": "लक्ष्य कॉन्फ़िगर करें और सुरक्षा आकलन चलाएं।", "results_title": "Red Team और Blue Team परिणाम",
        "results_subtitle": "चयनित रन के प्रॉम्प्ट और लक्ष्य मूल्यांकन।", "findings_title": "VAPT निष्कर्ष",
        "findings_subtitle": "पूर्ण आकलनों का नियम-आधारित प्रमाण विश्लेषण।", "reports": "रिपोर्ट",
        "reports_subtitle": "हितधारकों और ऑडिट के लिए रिपोर्ट बनाएं।", "integrations": "एकीकरण",
        "integrations_subtitle": "SecMate को सुरक्षा और रिपोर्टिंग टूल से जोड़ें।", "profile_subtitle": "अपनी पहचान और कार्यक्षेत्र भूमिका प्रबंधित करें।",
    },
    "Arabic": {
        "profile": "الملف الشخصي", "settings": "الإعدادات", "plan": "الخطة", "account_type": "نوع الحساب",
        "name": "الاسم", "language": "اللغة", "environment": "البيئة", "dashboard_density": "كثافة لوحة التحكم",
        "reduced_motion": "تقليل الحركة", "notifications": "الإشعارات", "no_notifications": "لا توجد إشعارات حتى الآن.",
        "mark_all_read": "تحديد الكل كمقروء", "clear": "مسح", "new": "جديد",
        "notification_ready_title": "مركز الإشعارات جاهز", "notification_ready_message": "ستظهر نتائج التقييم والتنبيهات الجديدة هنا.",
        "loading_title": "جارٍ تجهيز مساحة SecMate", "loading_subtitle": "جارٍ تحميل الإعدادات والتفضيلات.",
        "onboarding_kicker": "إعداد مساحة الأمان", "onboarding_title": "أعد أول تقييم أمان للذكاء الاصطناعي.",
        "onboarding_copy": "اربط الهدف وحدد التغطية وراجع النتائج ثم صدّر التقرير.",
        "step_connect": "ربط الهدف", "step_connect_desc": "أضف نقطة نهاية الوكيل وطريقة المصادقة.",
        "step_coverage": "اختيار التغطية", "step_coverage_desc": "اختر اختبارات Red Team وBlue Team وVAPT.",
        "step_findings": "مراجعة النتائج", "step_findings_desc": "تابع الخطورة والأدلة وسلوك الحماية.",
        "step_report": "تصدير التقرير", "step_report_desc": "أنشئ تقريراً جاهزاً لأصحاب المصلحة.",
        "about_use_case": "أخبرنا عن حالة الاستخدام", "user_type_question": "ما الوصف الأنسب لك؟",
        "use_case_question": "فيم ستستخدم SecMate؟", "goal_question": "هل تريد مساعدة محددة من SecMate؟",
        "goal_placeholder": "مثال: اختبار حقن التعليمات قبل نشر روبوت دعم.",
        "workspace_preferences": "تفضيلات مساحة العمل", "enter_dashboard": "فتح لوحة التحكم",
        "preferences_hint": "يتم حفظ هذه الخيارات لمساحة العمل ويمكن تغييرها لاحقاً.",
        "dashboard": "لوحة التحكم", "workspace": "مساحة العمل", "optimized_for": "محسّن من أجل",
        "new_assessment": "تقييم جديد", "workspace_health": "حالة مساحة العمل", "ready": "جاهز",
        "unread_notifications": "{count} إشعارات غير مقروءة", "settings_subtitle": "إدارة اللغة والبيئة ومظهر مساحة العمل.",
        "appearance": "المظهر", "theme": "السمة", "save_settings": "حفظ الإعدادات", "settings_saved": "تم حفظ إعدادات مساحة العمل.",
        "new_assessment_subtitle": "كوّن هدفاً وشغّل تقييماً أمنياً.", "results_title": "نتائج Red Team وBlue Team",
        "results_subtitle": "المطالبات وتقييمات الهدف للتشغيل المحدد.", "findings_title": "نتائج VAPT",
        "findings_subtitle": "تحليل الأدلة للتقييمات المكتملة.", "reports": "التقارير",
        "reports_subtitle": "إنشاء تقارير لأصحاب المصلحة والتدقيق.", "integrations": "عمليات التكامل",
        "integrations_subtitle": "ربط SecMate بأدوات الأمان والتقارير.", "profile_subtitle": "إدارة هويتك ودورك في مساحة العمل.",
    },
    "French": {
        "profile": "Profil", "settings": "Paramètres", "plan": "Forfait", "account_type": "Type de compte",
        "name": "Nom", "language": "Langue", "environment": "Environnement", "dashboard_density": "Densité du tableau de bord",
        "reduced_motion": "Réduire les animations", "notifications": "Notifications", "no_notifications": "Aucune notification.",
        "mark_all_read": "Tout marquer comme lu", "clear": "Effacer", "new": "Nouveau",
        "notification_ready_title": "Centre de notifications prêt", "notification_ready_message": "Les évaluations et nouveaux résultats apparaîtront ici.",
        "loading_title": "Préparation de votre espace SecMate", "loading_subtitle": "Chargement de l'intégration et des préférences.",
        "onboarding_kicker": "CONFIGURATION DE L'ESPACE SÉCURITÉ", "onboarding_title": "Configurez votre première évaluation de sécurité IA.",
        "onboarding_copy": "Connectez une cible, choisissez la couverture, examinez les résultats et exportez le rapport.",
        "step_connect": "Connecter la cible", "step_connect_desc": "Ajoutez le point de terminaison et la méthode d'authentification.",
        "step_coverage": "Choisir la couverture", "step_coverage_desc": "Sélectionnez les contrôles Red Team, Blue Team et VAPT.",
        "step_findings": "Examiner les résultats", "step_findings_desc": "Suivez la gravité, les preuves et les garde-fous.",
        "step_report": "Exporter le rapport", "step_report_desc": "Créez un rapport prêt pour les parties prenantes.",
        "about_use_case": "Parlez-nous de votre usage", "user_type_question": "Quel profil vous décrit le mieux ?",
        "use_case_question": "Comment utiliserez-vous SecMate ?", "goal_question": "Un besoin particulier pour SecMate ?",
        "goal_placeholder": "Exemple : tester l'injection de prompt avant de déployer un bot de support.",
        "workspace_preferences": "Préférences de l'espace", "enter_dashboard": "Ouvrir le tableau de bord",
        "preferences_hint": "Ces choix sont enregistrés pour cet espace et peuvent être modifiés plus tard.",
        "dashboard": "Tableau de bord", "workspace": "espace", "optimized_for": "Optimisé pour",
        "new_assessment": "Nouvelle évaluation", "workspace_health": "État de l'espace", "ready": "prêt",
        "unread_notifications": "{count} notifications non lues", "settings_subtitle": "Gérez la langue, l'environnement et l'apparence.",
        "appearance": "Apparence", "theme": "Thème", "save_settings": "Enregistrer", "settings_saved": "Les paramètres ont été appliqués.",
        "new_assessment_subtitle": "Configurez une cible et lancez une évaluation de sécurité.", "results_title": "Résultats Red Team et Blue Team",
        "results_subtitle": "Prompts et évaluations de la cible pour l'exécution sélectionnée.", "findings_title": "Résultats VAPT",
        "findings_subtitle": "Analyse des preuves pour les évaluations terminées.", "reports": "Rapports",
        "reports_subtitle": "Générez des rapports pour les parties prenantes et les audits.", "integrations": "Intégrations",
        "integrations_subtitle": "Connectez SecMate aux outils de sécurité et de reporting.", "profile_subtitle": "Gérez votre identité et votre rôle dans l'espace.",
    },
}


OPTION_LABELS = {
    "Hindi": {
        "Staging": "स्टेजिंग", "Production": "प्रोडक्शन", "Local": "लोकल",
        "Comfortable": "आरामदायक", "Compact": "संक्षिप्त", "Spacious": "विस्तृत",
        "Student": "छात्र", "Engineer": "इंजीनियर", "Working Professional": "कार्यरत पेशेवर",
        "Security Analyst": "सुरक्षा विश्लेषक", "Founder / Product Owner": "संस्थापक / उत्पाद स्वामी", "Other": "अन्य",
        "Learning AI security": "AI सुरक्षा सीखना", "Testing an internal AI agent": "आंतरिक AI एजेंट का परीक्षण",
        "Client security assessments": "क्लाइंट सुरक्षा आकलन", "Compliance and audit reports": "अनुपालन और ऑडिट रिपोर्ट",
        "Research and experimentation": "अनुसंधान और प्रयोग", "Production monitoring": "प्रोडक्शन निगरानी",
    },
    "Arabic": {
        "Staging": "اختبار", "Production": "إنتاج", "Local": "محلي",
        "Comfortable": "مريح", "Compact": "مضغوط", "Spacious": "واسع",
        "Student": "طالب", "Engineer": "مهندس", "Working Professional": "محترف",
        "Security Analyst": "محلل أمني", "Founder / Product Owner": "مؤسس / مالك منتج", "Other": "أخرى",
        "Learning AI security": "تعلم أمان الذكاء الاصطناعي", "Testing an internal AI agent": "اختبار وكيل داخلي",
        "Client security assessments": "تقييمات أمان العملاء", "Compliance and audit reports": "تقارير الامتثال والتدقيق",
        "Research and experimentation": "البحث والتجربة", "Production monitoring": "مراقبة الإنتاج",
    },
    "French": {
        "Staging": "Préproduction", "Production": "Production", "Local": "Local",
        "Comfortable": "Confortable", "Compact": "Compact", "Spacious": "Aéré",
        "Student": "Étudiant", "Engineer": "Ingénieur", "Working Professional": "Professionnel",
        "Security Analyst": "Analyste sécurité", "Founder / Product Owner": "Fondateur / Responsable produit", "Other": "Autre",
        "Learning AI security": "Apprendre la sécurité IA", "Testing an internal AI agent": "Tester un agent IA interne",
        "Client security assessments": "Évaluations de sécurité client", "Compliance and audit reports": "Conformité et audit",
        "Research and experimentation": "Recherche et expérimentation", "Production monitoring": "Surveillance de production",
    },
}


def initialize_workspace_state():
    """Initialize stable session keys used by all workspace controls."""
    st.session_state.setdefault("dashboard_theme", "SecMate Dark")
    st.session_state.setdefault("language_pref", "English")
    st.session_state.setdefault("workspace_environment", "Staging")
    st.session_state.setdefault("dashboard_density", "Comfortable")
    st.session_state.setdefault("reduced_motion", False)
    st.session_state.setdefault("onboarding_user_type", "Security Analyst")
    st.session_state.setdefault("onboarding_use_case", "Testing an internal AI agent")
    st.session_state.setdefault("onboarding_goal", "")
    st.session_state.setdefault("workspace_profiles", {})


def t(key: str, **values) -> str:
    """Translate a UI string, falling back to English."""
    initialize_workspace_state()
    language = st.session_state.get("language_pref", "English")
    template = TEXT.get(language, {}).get(key, TEXT["English"].get(key, key))
    return template.format(**values)


def option_label(value: str) -> str:
    """Return a localized display label while preserving a stable value."""
    initialize_workspace_state()
    language = st.session_state.get("language_pref", "English")
    return OPTION_LABELS.get(language, {}).get(value, value)


def save_workspace_profile():
    """Persist onboarding and workspace preferences for the signed-in email."""
    initialize_workspace_state()
    email = st.session_state.get("user_email")
    if not email:
        return
    st.session_state.workspace_profiles[email] = {
        "user_type": st.session_state.get("onboarding_user_type", "Security Analyst"),
        "use_case": st.session_state.get("onboarding_use_case", "Testing an internal AI agent"),
        "goal": st.session_state.get("onboarding_goal", ""),
        "language": st.session_state.get("language_pref", "English"),
        "environment": st.session_state.get("workspace_environment", "Staging"),
        "density": st.session_state.get("dashboard_density", "Comfortable"),
        "theme": st.session_state.get("dashboard_theme", "SecMate Dark"),
        "reduced_motion": st.session_state.get("reduced_motion", False),
    }


def load_workspace_profile(email: str) -> bool:
    """Load a previously completed onboarding profile for an email."""
    initialize_workspace_state()
    profile = st.session_state.workspace_profiles.get(email)
    if not profile:
        return False
    st.session_state.onboarding_user_type = profile.get("user_type", "Security Analyst")
    st.session_state.onboarding_use_case = profile.get("use_case", "Testing an internal AI agent")
    st.session_state.onboarding_goal = profile.get("goal", "")
    st.session_state.language_pref = profile.get("language", "English")
    st.session_state.workspace_environment = profile.get("environment", "Staging")
    st.session_state.dashboard_density = profile.get("density", "Comfortable")
    st.session_state.dashboard_theme = profile.get("theme", "SecMate Dark")
    st.session_state.reduced_motion = profile.get("reduced_motion", False)
    return True


def persist_workspace_preferences():
    """Update preference fields in an existing onboarding profile."""
    initialize_workspace_state()
    email = st.session_state.get("user_email")
    profile = st.session_state.workspace_profiles.get(email) if email else None
    if not profile:
        return
    profile.update(
        language=st.session_state.language_pref,
        environment=st.session_state.workspace_environment,
        density=st.session_state.dashboard_density,
        theme=st.session_state.dashboard_theme,
        reduced_motion=st.session_state.reduced_motion,
    )
