import streamlit as st
import requests
import time
import os
print("Current directory:", os.getcwd())
print("Files in directory:", os.listdir())

# Initialize session state
if 'lang' not in st.session_state:
    st.session_state.lang = 'en'
if 'skills' not in st.session_state:
    st.session_state.skills = []

# Set page configuration
st.set_page_config(page_title="Green Matchers", page_icon="🌱", layout="centered")




translations = {
    "en": {
        "title": "🌱 Green Matchers: AI-Powered Eco Job Revolution",
        "select_skills": "Select your skills (or type new ones):",
        "button": "Discover Green Jobs & Stories",
        "matches_header": "View Job Matches",
        "story_header": "Read Your Green Story",
        "no_matches": "No matches found—add more jobs via backend!",
        "enter_skills": "Please select or enter at least one skill!",
        "error": "Error: {error} - Ensure backend is running at http://127.0.0.1:8000!",
        "success": "Matches found!",
        "time_help": "Time & Help",
        "search": "Search",
        "certificate": "Certification",
        "ai_internship": "AI Internship",
        "company": "Company",
        "project": "Projects",
        "prompt_word": "Prompt",
        "language": "Select Language",
        "personal_details": "Personal Details"        
    },
    "hi": {
        "title": "🌱 ग्रीन मैचर्स: AI-संचालित पर्यावरणीय नौकरी क्रांति",
        "select_skills": "अपनी स्किल्स चुनें (या नई जोड़ें):",
        "button": "ग्रीन जॉब्स और कहानियां खोजें",
        "matches_header": "जॉब मैच देखें",
        "story_header": "अपनी ग्रीन कहानी पढ़ें",
        "no_matches": "कोई मैच नहीं मिला—बैकएंड के माध्यम से अधिक जॉब्स जोड़ें!",
        "enter_skills": "कृपया कम से कम एक स्किल चुनें या दर्ज करें!",
        "error": "त्रुटि: {error} - सुनिश्चित करें कि बैकएंड http://127.0.0.1:8000 पर चल रहा है!",
        "success": "मैच मिल गए!",
        "time_help": "समय और सहायता",
        "search": "खोज",
        "certificate": "प्रमाणपत्र",
        "ai_internship": "AI इंटर्नशिप",
        "company": "कंपनी",
        "project": "परियोजनाएं",
        "prompt_word": "प्रॉम्प्ट",
        "language": "भाषा चुनें",
        "personal_details": "व्यक्तिगत विवरण"
    },
    "bn": {
        "title": "🌱 গ্রিন ম্যাচার্স: এআই-চালিত ইকো জব বিপ্লব",
        "select_skills": "আপনার দক্ষতা নির্বাচন করুন (নতুন যোগ করুন):",
        "button": "গ্রিন চাকরি এবং গল্প আবিষ্কার করুন",
        "matches_header": "চাকরির মিল দেখুন",
        "story_header": "আপনার গ্রিন গল্প পড়ুন",
        "no_matches": "কোনো মিল পাওয়া যায়নি—ব্যাকএন্ডের মাধ্যমে আরও চাকরি যোগ করুন!",
        "enter_skills": "দয়া করে কমপক্ষে একটি দক্ষতা নির্বাচন করুন বা লিখুন!",
        "error": "ত্রুটি: {error} - নিশ্চিত করুন যে ব্যাকএন্ড http://127.0.0.1:8000 চলছে!",
        "success": "মিল পাওয়া গেছে!",
        "time_help": "সময় এবং সাহায্য",
        "search": "অনুসন্ধান",
        "certificate": "প্রমাণপত্র",
        "ai_internship": "AI ইন্টার্নশিপ",
        "company": "কোম্পানি",
        "project": "প্রকল্প",
        "prompt_word": "প্রম্পট",
        "language": "ভাষা নির্বাচন করুন",
        "personal_details": "ব্যক্তিগত বিবরণ"
    },
    "mr": {
        "title": "🌱 ग्रीन मॅचर्स: AI-द्वारे चालित इको नोकरी क्रांती",
        "select_skills": "तुमच्या कौशल्यांचा निवडा (किंवा नवीन जोडा):",
        "button": "ग्रीन नोकऱ्या आणि कथा शोधा",
        "matches_header": "नोकरी मॅच पहा",
        "story_header": "तुमची ग्रीन कथा वाचा",
        "no_matches": "कोणताही मॅच सापडला नाही—बॅकएंडद्वारे अधिक नोकऱ्या जोडा!",
        "enter_skills": "कृपया किमान एक कौशल्य निवडा किंवा टाका!",
        "error": "त्रुटी: {error} - सुनिश्चित करा की बॅकएंड http://127.0.0.1:8000 वर चालू आहे!",
        "success": "मॅच सापडले!",
        "time_help": "वेळ आणि मदत",
        "search": "शोध",
        "certificate": "प्रमाणपत्र",
        "ai_internship": "AI इंटर्नशिप",
        "company": "कंपनी",
        "project": "प्रकल्प",
        "prompt_word": "प्रॉम्प्ट",
        "language": "भाषा निवडा",
        "personal_details": "वैयक्तिक तपशील"
    },
    "te": {
        "title": "🌱 గ్రీన్ మ్యాచర్స్: AI-చేత నడిచే ఎకో ఉద్యోగ విప్లవం",
        "select_skills": "మీ నైపుణ్యాలను ఎంచుకోండి (కొత్తవి జోడించండి):",
        "button": "గ్రీన్ ఉద్యోగాలు మరియు కథలు కనుగొనండి",
        "matches_header": "ఉద్యోగ మ్యాచ్‌లు చూడండి",
        "story_header": "మీ గ్రీన్ కథను చదవండి",
        "no_matches": "మ్యాచ్‌లు లేవు—బ్యాకెండ్ ద్వారా మరిన్ని ఉద్యోగాలు జోడించండి!",
        "enter_skills": "దయచేసి కనీసం ఒక నైపుణ్యాన్ని ఎంచుకోండి లేదా ఎంటర్ చేయండి!",
        "error": "పొర్పు: {error} - బ్యాకెండ్ http://127.0.0.1:8000 పై రన్ అవుతున్నట్లు నిర్ధారించండి!",
        "success": "మ్యాచ్‌లు కనుగొనబడ్డాయి!",
        "time_help": "సమయం మరియు సహాయం",
        "search": "సెర్చ్",
        "certificate": "సర్టిఫికెట్",
        "ai_internship": "AI ఇంటర్న్‌షిప్",
        "company": "కంపెనీ",
        "project": "ప్రాజెక్ట్‌లు",
        "prompt_word": "ప్రాంప్ట్",
        "language": "భాషను ఎంచుకోండి",
        "personal_details": "వ్యక్తిగత వివరాలు"
    },
    "ta": {
        "title": "🌱 பசுமை பொருத்தங்கள்: AI-ஆல் இயக்கப்படும் பசுமை வேலைவாய்ப்பு புரட்சி",
        "select_skills": "உங்கள் திறன்களைத் தேர்ந்தெடுக்கவும் (புதியவற்றை உள்ளிடவும்):",
        "button": "பசுமை வேலைகள் மற்றும் கதைகளை கண்டறி",
        "matches_header": "வேலை பொருத்தங்களை பார்",
        "story_header": "உங்கள் பசுமை கதையை படி",
        "no_matches": "பொருத்தங்கள் இல்லை—பின்னணி மூலம் மேலும் வேலைகளை சேர்க்கவும்!",
        "enter_skills": "குறைந்தது ஒரு திறமையைத் தேர்ந்தெடுக்கவும் அல்லது உள்ளிடவும்!",
        "error": "பிழை: {error} - பின்னணி http://127.0.0.1:8000 இல் இயங்குவதை உறுதி செய்யவும்!",
        "success": "பொருத்தங்கள் கிடைத்தன!",
        "time_help": "நேரம் மற்றும் உதவி",
        "search": "தேடல்",
        "certificate": "சான்றிதழ்",
        "ai_internship": "AI இன்டர்ன்ஷிப்",
        "company": "நிறுவனம்",
        "project": "திட்டங்கள்",
        "prompt_word": "குறிப்பு",
        "language": "மொழியை தேர்ந்தெடுக்கவும்",
        "personal_details": "வ్యக்திஇதழ் விவரங்கள்"
    },
    "gu": {
        "title": "🌱 ગ્રીન મેચર્સ: AI-દ્વારા ચલાવવામાં આવતી ઇકો જોબ ક્રાંતિ",
        "select_skills": "તમારી કુશળતાઓ પસંદ કરો (અથવા નવી ઉમેરો):",
        "button": "ગ્રીન જોબ્સ અને વાર્તાઓ શોધો",
        "matches_header": "જોબ મેચ જુઓ",
        "story_header": "તમારી ગ્રીન વાર્તા વાંચો",
        "no_matches": "કોઈ મેચ મળ્યું નથી—બેકએન્ડ દ્વારા વધુ જોબ્સ ઉમેરો!",
        "enter_skills": "કૃપા કરીને ઓછામાં ઓછું એક કુશળતા પસંદ કરો અથવા લખો!",
        "error": "ભૂલ: {error} - ખાતરી કરો કે બેકએન્ડ http://127.0.0.1:8000 પર ચાલી રહ્યું છે!",
        "success": "મેચ મળ્યા!",
        "time_help": "સમય અને મદદ",
        "search": "શોધ",
        "certificate": "પ્રમાણપત્ર",
        "ai_internship": "AI ઇન્ટર્નશિપ",
        "company": "કંપની",
        "project": "પ્રોજેક્ટ્સ",
        "prompt_word": "પ્રોમ્પ્ટ",
        "language": "ભાષા પસંદ કરો",
        "personal_details": "વ્યક્તિગત વિગતો"
    },
    "ur": {
        "title": "🌱 گرین میچرز: AI سے چلنے والی ایکو جاب انقلاب",
        "select_skills": "اپنی مہارتیں منتخب کریں (یا نئی شامل کریں):",
        "button": "گرین جابز اور کہانیاں تلاش کریں",
        "matches_header": "جاب میچ دیکھیں",
        "story_header": "اپنی گرین کہانی پڑھیں",
        "no_matches": "کوئی میچ نہیں ملا—بیک اینڈ کے ذریعے مزید جابز شامل کریں!",
        "enter_skills": "براہ مہربانی کم از کم ایک مہارت منتخب کریں یا درج کریں!",
        "error": "غلطی: {error} - یقینی بنائیں کہ بیک اینڈ http://127.0.0.1:8000 پر چل رہا ہے!",
        "success": "میچ مل گئے!",
        "time_help": "وقت اور مدد",
        "search": "تلاش",
        "certificate": "سرٹیفکیٹ",
        "ai_internship": "AI انٹرنشپ",
        "company": "کمپنی",
        "project": "پروجیکٹس",
        "prompt_word": "پرومپٹ",
        "language": "زبان منتخب کریں",
        "personal_details": "ذاتی تفصیلات"
    },
    "kn": {
        "title": "🌱 ಗ್ರೀನ್ ಮ್ಯಾಚರ್ಸ್: AI-ಚಾಲಿತ ಇಕೋ ಉದ್ಯೋಗ ಕ್ರಾಂತಿ",
        "select_skills": "ನಿಮ್ಮ ಕೌಶಲ್ಯಗಳನ್ನು ಆಯ್ಕೆಮಾಡಿ (ಅಥವಾ ಹೊಸದನ್ನು ಸೇರಿಸಿ):",
        "button": "ಗ್ರೀನ್ ಉದ್ಯೋಗಗಳು ಮತ್ತು ಕಥೆಗಳನ್ನು ಕಂಡುಹಿಡಿಯಿರಿ",
        "matches_header": "ಉದ್ಯೋಗ ಹೊಂದಾಣಿಕೆಗಳನ್ನು ನೋಡಿ",
        "story_header": "ನಿಮ್ಮ ಗ್ರೀನ್ ಕಥೆಯನ್ನು ಓದಿ",
        "no_matches": "ಹೊಂದಾಣಿಕೆಗಳು ದೊರೆತಿಲ್ಲ—ಬ್ಯಾಕೆಂಡ್ ಮೂಲಕ ಹೆಚ್ಚು ಉದ್ಯೋಗಗಳನ್ನು ಸೇರಿಸಿ!",
        "enter_skills": "ದಯವಿಟ್ಟು ಕನಿಷ್ಠ ಒಂದು ಕೌಶಲ್ಯವನ್ನು ಆಯ್ಕೆಮಾಡಿ ಅಥವಾ ನಮೂದಿಸಿ!",
        "error": "ದೋಷ: {error} - ಬ್ಯಾಕೆಂಡ್ http://127.0.0.1:8000 ನಲ್ಲಿ ಚಲಿಸುತ್ತಿದೆಯೆಂದು ಖಚಿತಪಡಿಸಿ!",
        "success": "ಹೊಂದಾಣಿಕೆಗಳು ಸಿಕ್ಕಿವೆ!",
        "time_help": "ಸಮಯ ಮತ್ತು ಸಹಾಯ",
        "search": "ಹುಡುಕಾಟ",
        "certificate": "ಪ್ರಮಾಣಪತ್ರ",
        "ai_internship": "AI ಇಂಟರ್ನ್‌ಶಿಪ್",
        "company": "ಕಂಪನಿ",
        "project": "ಪ್ರಾಜೆಕ್ಟ್‌ಗಳು",
        "prompt_word": "ಪ್ರಾಂಪ್ಟ್",
        "language": "ಭಾಷೆ ಆಯ್ಕೆಮಾಡಿ",
        "personal_details": "ವ್ಯಕ್ತಿಗತ ವಿವರಗಳು"
    },
    "or": {
        "title": "🌱 ଗ୍ରିନ୍ ମ୍ୟାଚର୍ସ: AI-ଦ୍ୱାରା ଚାଲିତ ଇକୋ ଜବ୍ ବିପ୍ଳବ",
        "select_skills": "ତୁମର ସ୍କିଲ୍ଗୁଡ଼ିକୁ ବାଛନ୍ତୁ (ନାହିଁତେ ନୂଆ ଯୋଡ଼ନ୍ତୁ):",
        "button": "ଗ୍ରିନ୍ ଜବ୍ ଏବଂ କାହାଣୀ ଖୋଜନ୍ତୁ",
        "matches_header": "ଜବ୍ ମ୍ୟାଚ ଦେଖନ୍ତୁ",
        "story_header": "ତୁମର ଗ୍ରିନ୍ କାହାଣୀ ପଢ଼ନ୍ତୁ",
        "no_matches": "କୌଣସି ମ୍ୟାଚ୍ ମିଳିଲା ନାହିଁ—ବ୍ୟାକେଣ୍ଡ ମାଧ୍ୟମରେ ଅଧିକ ଜବ୍ ଯୋଡ଼ନ୍ତୁ!",
        "enter_skills": "ଦୟାକରି ଅତି କମରେ ଏକ ସ୍କିଲ୍ ବାଛନ୍ତୁ କିମ୍ବା ଲେଖନ୍ତୁ!",
        "error": "ତ୍ରୁଟି: {error} - ନିଶ୍ଚିତ କରନ୍ତୁ ଯେ ବ୍ୟାକେଣ୍ଡ http://127.0.0.1:8000 ଚାଲୁ ଅଛି!",
        "success": "ମ୍ୟାଚ୍ ମିଳିଲା!",
        "time_help": "ସମୟ ଏବଂ ସାହାଯ୍ୟ",
        "search": "ଖୋଜ",
        "certificate": "ପ୍ରମାଣପତ୍ର",
        "ai_internship": "AI ଇନ୍ଟର୍ନଶିପ",
        "company": "କମ୍ପାନୀ",
        "project": "ପ୍ରକଳ୍ପ",
        "prompt_word": "ପ୍ରମ୍ପ୍ଟ",
        "language": "ଭାଷା ଚୟନ କରନ୍ତୁ",
        "personal_details": "ବ୍ୟକ୍ତିଗତ ବିବରଣୀ"
    },
    "ml": {
        "title": "🌱 ഗ്രീൻ മാച്ചേഴ്സ്: AI-ന്‍റെ സഹായത്തോടെ പരിസ്ഥിതി സൗഹൃദ ജോലി വിപ്ലവം",
        "select_skills": "നിങ്ങളുടെ കഴിവുകൾ തിരഞ്ഞെടുക്കുക (അല്ലെങ്കിൽ പുതിയത് ചേർക്കുക):",
        "button": "ഗ്രീൻ ജോലികളും കഥകളും കണ്ടെത്തുക",
        "matches_header": "ജോലി മാച്ചുകൾ കാണുക",
        "story_header": "നിങ്ങളുടെ ഗ്രീൻ കഥ വായിക്കുക",
        "no_matches": "മാച്ചുകൾ കിട്ടിയില്ല—ബാക്ക്‌എൻഡ് വഴി കൂടുതൽ ജോലികൾ ചേർക്കുക!",
        "enter_skills": "ദയവായി കുറഞ്ഞത് ഒരു കഴിവ് തിരഞ്ഞെടുക്കുക അല്ലെങ്കിൽ നൽകുക!",
        "error": "പിശക്: {error} - ബാക്ക്‌എൻഡ് http://127.0.0.1:8000-ൽ പ്രവർത്തിക്കുന്നുണ്ടെന്ന് ഉറപ്പാക്കുക!",
        "success": "മാച്ചുകൾ കിട്ടി!",
        "time_help": "സമയവും സഹായവും",
        "search": "തിരയൽ",
        "certificate": "സർട്ടിഫിക്കറ്റ്",
        "ai_internship": "AI ഇന്റർന്ഷിപ്പ്",
        "company": "കമ്പനി",
        "project": "പദ്ധതികൾ",
        "prompt_word": "പ്രോംപ്റ്റ്",
        "language": "ഭാഷ തിരഞ്ഞെടുക്കുക",
        "personal_details": "വ്യക്തിഗത വിവരങ്ങൾ"
    }
}




# Custom CSS for navigation bar and existing styling
st.markdown("""
    <style>
    .header-container {
        display: flex;
        align-items: center;
        background: linear-gradient(90deg, #00695c 0%, #009688 100%);
        padding: 5px 20px;
        border-radius: 15px;
        margin-bottom: 20px;
        box-shadow: 0 6px 20px rgba(0,0,0,0.15);
        animation: fadeIn 1s ease-in;
    }
    .navbar {
        display: flex;
        align-items: center;
        margin-top: 40px;
        margin-left: 50px;
    }
    
    .navbar a, .navbar button {
        background: #ff9800;
        color: white;
        text-decoration: none;
        margin: 0px 8px;
        border-radius:15px;
        font-family: Arial, sans-serif;
        font-size: 16px;
        padding: 5px 10px;
        border-radius: 5px;
        cursor: pointer;
        display: inline-block; /* Ensure consistent box model */
        vertical-align: middle; /* Align text vertically */
    }
    .navbar a:hover, .navbar button {
        background-color: #f57c00;    
    }
    .navbar .dropdown {
        position: relative;
        display: inline-block;
    }
    .dropdown-content {
        display: none;
        position: absolute;
        min-width: 160px;
        box-shadow: 0 8px 16px rgba(0,0,0,0.2);
        z-index: 1;
        border-radius:10px;
    }
    .dropdown:hover .dropdown-content {
        display: block;
    }    
    .dropdown-content a {
        background-color: #ff9800;
        color: white;
        margin:5px 10px;
        padding:12px 16px;
        display: block;
        border-radius: 5px 15px;
        transition: background-color 0.3s ease;
    }
    .dropdown-content a:hover {
        background-color: #f57c00;
    }
            
    .highlight {
        background-color: #ff9800;
        padding: 5px 10px;
        border-radius: 5px;
    }
    .highlight:hover {
        background-color: #f57c00;
    }
            
    .login-btn {
        background: #ff9800;
        border: none;
        padding: 5px 15px;
        border-radius: 5px;
        cursor: pointer;
        font-size: 17px;
        height: 36px;
        line-height: 20px;
        transition: all 0.3s ease;
    }
    .login-btn:hover {
        background-color: #f57c00;
    }
    .profile-icon {
        width: 30px;
        height: 30px;
        border-radius: 50%;
        background-color: #fff;
        display: flex;
        align-items: center;
        justify-content: center;
        color: #00695c;
        font-weight: bold;
        margin-left: 15px;
    }
    .main {
        background: linear-gradient(135deg, #e0f7fa 0%, #b2dfdb 100%);
        padding: 20px;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
    @media (max-width: 100%) {
        .header-title { font-size: 30px; }
        .section-card { padding: 15px; }
        .stButton>button { font-size: 16px; padding: 10px 20px; }
        .main { padding: 10px; }
        .navbar a, .navbar button { margin: 0 10px; font-size: 14px; }
        .profile-icon { width: 25px; height: 25px; }
    }
    .header-title {
        font-size: 50px;
        font-weight: 700;
        margin-bottom: 15px;
        text-shadow: 3px 3px 6px rgba(0,0,0,0.4);
    }
    .section-card {
        background: linear-gradient(90deg, #00695c 0%, #009688 100%);
        padding: 10px;
        border-radius: 15px;
        box-shadow: 0 6px 18px rgba(0,0,0,0.15);
        margin-bottom: 20px;
        border-left: 6px solid #009688;
    }
    .section-card:hover {
        box-shadow: 0 10px 25px rgba(0,0,0,0.2);
    }
    .section-title {
        color: white;
        font-size: 26px;
        font-weight: 600;
        margin-bottom: 10px;
        display: flex;
        align-items: center;
    }
    .icon-box {
        background: #e0f7fa;
        color:black;
        padding: 20px;
        border-radius: 12px;
        text-align: center;
        margin: 15px 0;
        border: 2px solid #009688;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    .icon-box:hover {
        background: #b2dfdb;
        transform: translateY(-5px);
        box-shadow: 0 8px 20px rgba(0,0,0,0.2);
    }
    .stButton>button {
        background: linear-gradient(90deg, #00695c 0%, #009688 100%);
        color: black;
        border: none;
        padding: 15px 30px;
        border-radius: 10px;
        font-size: 20px;
        font-weight: 600;
        cursor: pointer;
        width: 100%;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background: linear-gradient(90deg, #004d40 0%, #00695c 100%);
        transform: scale(1.05);
        box-shadow: 0 8px 25px rgba(0,0,0,0.3);
        color:black;
    }
    </style>
""", unsafe_allow_html=True)

# Header with logo and navigation bar
col_logo, col_nav = st.columns([1, 5])  # col_logo for logo, col_nav for navigation
with col_logo:
    st.image("logo.png", width=80)
with col_nav:
    st.markdown("""
        <div class="navbar">
            <button onclick="window.scrollTo({top: 0, behavior: 'smooth'});">Home</button>
            <button onclick="document.getElementById('guidelines').scrollIntoView({behavior: 'smooth'});">Guidelines/Documentations</button>
            <button onclick="document.getElementById('support').scrollIntoView({behavior: 'smooth'});">Support</button>
            <button onclick="document.getElementById('compendium').scrollIntoView({behavior: 'smooth'});">Compendium</button>
            <button class="highlight" onclick="document.getElementById('youth_registration').scrollIntoView({behavior: 'smooth'});">Youth Registration</button>
            <button class="login-btn">Login</button>
            <div class="profile-icon">U</div> <!-- Placeholder for user profile icon -->
        </div>
                
    """, unsafe_allow_html=True)

t = translations[st.session_state.lang]
# Language selector (immediately after title area)
lang_options = ["en", "hi", "bn", "mr", "te", "ta", "gu", "ur", "kn", "or", "ml"]
lang_names = ["English", "हिंदी / Hindi", "বাংলা / Bengali", "मराठी / Marathi", "తెలుగు / Telugu", "தமிழ் / Tamil", "ગુજરાતી / Gujarati", "اردو / Urdu", "ಕನ್ನಡ / Kanada", "ଓଡ଼ିଆ", "മലയാളം / Malyalam"]

lang_index = lang_options.index(st.session_state.lang)
selected_lang = st.selectbox(t["language"], lang_names, index=lang_index, key="lang_select")
st.session_state.lang = lang_options[lang_names.index(selected_lang)] 


# Header title
st.markdown("----")

# Main Layout
col1, col2 = st.columns([1, 2])  # Left for placeholder, right for content

# AI instructor
with col1:
    st.markdown("<h3 style='color: #00695c; text-align: center; font-family: Arial, sans-serif; font-weight: bold;'>🤖 Green Matcher AI Assistant</h3>", unsafe_allow_html=True)
    
    # Initialize chat history in session state
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = [("AI", "Hi! I’m your Green Matcher AI. How can I help? Try 'How to get started' or 'What are green jobs?'")]

    # Display chat history
    for speaker, message in st.session_state.chat_history:
        bg_color = '#ff9800' if speaker == 'AI' else '#2979FF'
        text_align = 'left' if speaker == 'AI' else 'right'
        st.markdown(f"""
            <div style='margin: 5px; padding: 12px; border-radius: 15px; background-color: {bg_color}; color: white; text-align: {text_align}; 
            box-shadow: 0 4px 8px rgba(0,0,0,0.2); animation: fadeIn 0.5s ease-in; max-width: 70%;'>
            <b style='font-size: 16px;'>{speaker}:</b> {message}</div>
        """, unsafe_allow_html=True)

    # User input
    user_input = st.text_input("Ask me anything...", key="chat_input", placeholder="Type your question...")
    if user_input:
        from langchain_huggingface import HuggingFacePipeline
        from langchain.prompts import PromptTemplate
        from langchain.chains import ConversationChain
        from langchain.memory import ConversationBufferMemory
        from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
        import torch

        # Load a lightweight Hugging Face model
        model_id = "gpt2"
        tokenizer = AutoTokenizer.from_pretrained(model_id)
        model = AutoModelForCausalLM.from_pretrained(model_id)
        pipe = pipeline("text-generation", model=model, tokenizer=tokenizer, device=0 if torch.cuda.is_available() else -1, 
                        max_new_tokens=50, truncation=True, temperature=0.7, top_k=50)
        llm = HuggingFacePipeline(pipeline=pipe)

        # Define memory and prompt with history
        memory = ConversationBufferMemory()
        for speaker, message in st.session_state.chat_history:
            memory.chat_memory.add_user_message(message) if speaker == "User" else memory.chat_memory.add_ai_message(message)
        prompt = PromptTemplate(
            input_variables=["input", "lang", "history"],  # Added 'history' to match memory
            template="You are a friendly AI assistant for Green Matchers, a job-matching platform for green careers. Maintain context from previous messages: {history}. Provide concise, helpful responses in {lang}. User input: {input}"
        )

        # Get response
        chain = ConversationChain(llm=llm, memory=memory, prompt=prompt)
        response = chain.predict(input=user_input, lang=st.session_state.lang)

        # Update chat history
        st.session_state.chat_history.append(("User", user_input))
        st.session_state.chat_history.append(("AI", response[:200]))

        # Rerun to update display
        st.rerun()

    # Guidelines Section (expander for navigation)
    st.markdown(f'<div id="guidelines"></div>', unsafe_allow_html=True)
    with st.expander("Guidelines/Documentations"):
        st.write("How to use semantic AI for green jobs: Use 'Python web dev' to match 'back-end green intern'—bridges keyword biases for fairer access. Advances SDGs 8/10 by simulating 20% diverse hires.")

    # Support Section
    st.markdown(f'<div id="support"></div>', unsafe_allow_html=True)
    with st.expander("Support"):
        st.write("Contact us for help: shivamjaiswal.2024.cse@rajalakshmi.edu.in")

    # Compendium Section
    st.markdown(f'<div id="compendium"></div>', unsafe_allow_html=True)
    with st.expander("Compendium"):
        st.write("Collection of green job resources.")

    # Youth Registration Section
    st.markdown(f'<div id="youth_registration"></div>', unsafe_allow_html=True)
    with st.expander("Youth Registration"):
        st.write("Register for youth programs.")

    # About Section (new expander for team/SDGs)
    st.markdown(f'<div id="about"></div>', unsafe_allow_html=True)
    with st.expander("About"):
        st.write("Team Green Matchers: Shivam Jaiswal (backend/AI), Neha.R.N, Nishani.B, Mohamed Adhil.I. Advances SDGs 8/10 by simulating 20% diverse hires.")




with col2:
    tabs = st.tabs([t["personal_details"], t["certificate"], t["project"], t["ai_internship"], t["company"]])   
    # Personal Details Section
    with tabs[0]:
        st.markdown(f'<div class="section-card"><div class="section-title">🌱 {t["personal_details"]}</div>', unsafe_allow_html=True)
        with st.form("personal_details_form"):
            name = st.text_input("Name", key="name_input")
            email = st.text_input("Email", key="email_input")
            phone = st.text_input("Phone", key="phone_input")
            skills = st.multiselect("Skills", ["Python", "Django", "AI", "Renewable Energy", "Waste Management"], key="skills_input")
            profile_pic = st.file_uploader("Upload Profile Picture", type=["jpg", "png"], key="profile_pic_input")
            if profile_pic is not None:
                st.image(profile_pic, caption="Uploaded Profile Picture Preview", use_column_width=True)
            if st.form_submit_button("Save Details"):
                st.session_state.skills = skills  # Store skills in session state
                st.success("Personal details saved!")
                st.write(f"Selected skills: {skills}")
        st.markdown('</div>', unsafe_allow_html=True)

    # Certificate Section
    with tabs[1]: 
        st.markdown(f'<div class="section-card"><div class="section-title">🏆 {t["certificate"]}</div>', unsafe_allow_html=True)
        with st.form("certificate_form"):
            cert_name = st.text_input("Certificate Name", key="cert_name_input")
            cert_link = st.text_input("Link or Upload", key="cert_link_input")
            if st.form_submit_button("Add Certificate"):
                st.success(f"Added: {cert_name}")
                if "certificates" not in st.session_state:
                    st.session_state.certificates = []
                st.session_state.certificates.append({"name": cert_name, "link": cert_link})
        if "certificates" in st.session_state:
            st.write("**Your Certificates:**")
            for cert in st.session_state.certificates:
                st.write(f"- {cert['name']} ({cert['link']})")
        st.markdown('</div>', unsafe_allow_html=True)


    # Project Details Section
    with tabs[2]:
        st.markdown(f'<div class="section-card"><div class="section-title">🚀 {t["project"]}</div>', unsafe_allow_html=True)
        with st.form("project_form"):
            proj_title = st.text_input("Project Title", key="proj_title_input")
            proj_desc = st.text_area("Description", key="proj_desc_input")
            proj_link = st.text_input("GitHub/Link", key="proj_link_input")
            if st.form_submit_button("Add Project"):
                st.success(f"Added: {proj_title}")
                if "projects" not in st.session_state:
                    st.session_state.projects = []
                st.session_state.projects.append({"title": proj_title, "desc": proj_desc, "link": proj_link})
        if "projects" in st.session_state:
            st.write("**Your Projects:**")
            for proj in st.session_state.projects:
                st.write(f"- **{proj['title']}**: {proj['desc']} ({proj['link']})")
        st.markdown('</div>', unsafe_allow_html=True)

# AI internship section
    with tabs[3]:
        st.markdown(f'<div class="section-card"><div class="section-title">💼 {t["ai_internship"]}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="icon-box">🎓 Learn AI Skills<br/>Join Programs</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

# Company detail section
    with tabs[4]:
        st.markdown(f'<div class="section-card"><div class="section-title">🏢 {t["company"]}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="icon-box">🌟 Top Green Companies<br/>Explore Now</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)


    # Search Button
    if st.button(t["button"]):
        if st.session_state.get("skills"):  # Use skills from session state
            with st.spinner(t["success"]):
                try:
                    match_response = requests.post("http://127.0.0.1:8000/match_jobs", 
                                                   json={"skill_text": st.session_state.skills, "lang": st.session_state.lang},
                                                   timeout=10)
                    data = match_response.json()
                    matches = data.get("matches", [])
                    suggestions = data.get("suggestions", [])

                    

                    if matches:
                        st.toast(f"{t['success']} - {len(matches)} {t['matches_header'].lower()} found!", icon="✅")
                        st.success(t["success"])
                        st.markdown(f'<div class="section-card"><div class="section-title">✅ {t["matches_header"]}</div>', unsafe_allow_html=True)
                        for match in matches:
                            st.markdown(f"**{match['job_title']}** (Similarity: {match['similarity']:.2f})")
                            st.markdown(f"{match['description']}")
                            st.markdown("---")
                        st.markdown('</div>', unsafe_allow_html=True)
                    else:
                        st.warning(t["no_matches"])

                    if suggestions:
                        with st.expander("Upskilling Suggestions"):
                            st.markdown("### Suggested Skills to Improve Matches")
                            for sug in suggestions:
                                st.markdown(f"- {sug['skill']}: [Course Link]({sug['link']})")
                    
                    narrative_response = requests.post("http://127.0.0.1:8000/generate_narrative", 
                                                       json={"skill_text": st.session_state.skills, "lang": st.session_state.lang})
                    narrative = narrative_response.json()["narrative"]
                    st.markdown(f'<div class="section-card"><div class="section-title">📖 {t["story_header"]}</div>{narrative}</div>', unsafe_allow_html=True)

                except requests.exceptions.Timeout:
                    st.error(t["error"].format(error="Request timed out"))    
                except Exception as e:
                    st.error(t["error"].format(error=str(e)))
        else:
            st.warning(t["enter_skills"])

            
    # Real-time Notifications
    st.markdown("""
        <script>
        const ws = new WebSocket("ws://127.0.0.1:8000/ws");
        ws.onmessage = function(event) {
            const notifications = document.getElementById("notifications");
            notifications.innerHTML += `<p>${event.data}</p>`;
        };
        ws.onerror = function(error) {
            console.error("WebSocket error:", error);
        };
        ws.onclose = function() {
            console.log("WebSocket closed");
        };
        </script>
        <div id="notifications" style="background-color: #f0f0f0; padding: 10px; border-radius: 5px; margin-top: 20px;">
            <h3>Notifications</h3>
        </div>
    """, unsafe_allow_html=True)

# Bottom Section
st.markdown("---")
bottom_col1, bottom_col2 = st.columns(2)

with bottom_col1:
    st.markdown(f'<div class="section-card"><div class="section-title">🚀 {t["project"]}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="icon-box">📊 Browse Projects<br/>Green Initiatives</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with bottom_col2:
    st.markdown(f'<div class="section-card"><div class="section-title">💬 {t["prompt_word"]}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="icon-box">✍️ AI Chat Assistant<br/>Ask Questions</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# PWA Support
st.markdown("""
<link rel="manifest" href="/manifest.json">
<script>
  if ('serviceWorker' in navigator) {
    navigator.serviceWorker.register('/service-worker.js')
      .then(() => console.log('Service Worker registered'))
      .catch(err => console.log('Service Worker error:', err));
  }
</script>
""", unsafe_allow_html=True)




