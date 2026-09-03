#!/usr/bin/env python3
# Build the English template (artifact-en.html) from the finished Arabic template,
# reusing the existing English copy from the old EN artifact.
import re
import os
HERE=os.path.dirname(os.path.abspath(__file__))
AR=open(os.path.join(HERE,'artifact-ar.html'),encoding='utf-8').read()
ENOLD=open(os.path.join(HERE,'artifact-en.old.html'),encoding='utf-8').read()
h=AR

# ---- 1) structural ----
h=h.replace('<title>نواف الشريف — انظمة بيانات واتمتة اعمال</title>','<title>Nawaf Al-Shareif — Data Systems & Automation</title>')
h=h.replace('family=IBM+Plex+Sans+Arabic:wght@300;400;500;600;700&family=IBM+Plex+Mono',
            'family=IBM+Plex+Sans:wght@300;400;500;600;700&family=IBM+Plex+Sans+Arabic:wght@300;400;500;600;700&family=IBM+Plex+Mono')
h=h.replace("--sans:'IBM Plex Sans Arabic','IBM Plex Sans',system-ui,sans-serif;",
            "--sans:'IBM Plex Sans','IBM Plex Sans Arabic',system-ui,sans-serif;")
h=h.replace('.page-rtl{direction:rtl}','.page-en{direction:ltr}')
h=h.replace('<div class="page-rtl" dir="rtl" lang="ar">','<div class="page-en" dir="ltr" lang="en">')
h=h.replace("document.documentElement.lang==='en'","true")
h=h.replace("document.dir==='rtl'","false")
# lang toggle links -> point to AR
h=h.replace('href="https://claude.ai/code/artifact/30946092-ea26-49a1-8604-75b38b28c00d" target="_blank" rel="noopener">EN</a>',
            'href="https://claude.ai/code/artifact/51297c92-5e4d-4350-adf1-a5a5d11a2e20" target="_blank" rel="noopener">عربي</a>')
h=h.replace('href="https://claude.ai/code/artifact/30946092-ea26-49a1-8604-75b38b28c00d" target="_blank" rel="noopener">English</a>',
            'href="https://claude.ai/code/artifact/51297c92-5e4d-4350-adf1-a5a5d11a2e20" target="_blank" rel="noopener">العربية</a>')

# ---- 2) swap ARCHIVE list (English, same structure) ----
arch=re.search(r'<div class="arch-list">.*?</div>\n</section>', ENOLD, re.S).group(0)
EN_ARCH_P7='''<article class="arow" data-cat="sys">
      <button class="arow-head" type="button" aria-expanded="false">
        <span class="t">Full elevator-maintenance web system where the contract generates the work</span>
        <span class="side"><span class="cat">Operations systems</span><span class="stat num">35</span><span class="chev">+</span></span>
      </button>
      <div class="arow-body"><div class="arow-in"><div class="arow-pad">
        <div>
          <div class="part"><b>The problem</b><p>Operating a large elevator fleet ran on paper and WhatsApp: different maintenance cycles computed by hand, technician reports lost in messages, and contracts expiring unnoticed.</p></div>
          <div class="part"><b>The system</b><p>The contract is the engine: it auto-generates each month&#39;s tasks for every due elevator and stops them when it expires. A 15-section admin panel, a mobile field panel with a 35-item inspection checklist, and an official report reproducing the company&#39;s own approved form.</p></div>
          <div class="part"><b>The result</b><p>One source of truth: a month&#39;s tasks in one click, every visit documented with its report, and contracts nearing expiry visible before it&#39;s too late.</p></div>
        </div>
        <div class="quote">Elevator maintenance company · Jeddah<div class="who">Web system · two interfaces, one database</div></div>
      </div></div></div>
    </article>

    '''
arch=arch.replace('<div class="arch-list">\n\n    ','<div class="arch-list">\n\n    '+EN_ARCH_P7,1)
h=re.sub(r'<div class="arch-list">.*?</div>\n</section>', lambda m: arch, h, flags=re.S)

# ---- 3) swap CASE-DATA (English) + inject galleries ----
GAL={
'p1':'<div class="cgallery"><img class="cg-main" src="__G_P1_1__" alt="Sales & inventory dashboard">\n      <div class="cg-thumbs">\n        <button class="cg-th on" type="button" data-full="__G_P1_1__"><img src="__G_P1_1__" alt=""></button>\n        <button class="cg-th" type="button" data-full="__G_P1_2__"><img src="__G_P1_2__" alt=""></button>\n      </div></div>',
'p2':'<div class="cgallery"><img class="cg-main" src="__G_P2_1__" alt="Permits monitoring dashboard"></div>',
'p3':'<div class="cgallery"><img class="cg-main" src="__G_P3_1__" alt="Operating system">\n      <div class="cg-thumbs">\n        <button class="cg-th on" type="button" data-full="__G_P3_1__"><img src="__G_P3_1__" alt=""></button>\n        <button class="cg-th" type="button" data-full="__G_P3_2__"><img src="__G_P3_2__" alt=""></button>\n      </div></div>',
'p4':'<div class="cgallery"><img class="cg-main" src="__G_P4_1__" alt="Feasibility study">\n      <div class="cg-thumbs">\n        <button class="cg-th on" type="button" data-full="__G_P4_1__"><img src="__G_P4_1__" alt=""></button>\n        <button class="cg-th" type="button" data-full="__G_P4_2__"><img src="__G_P4_2__" alt=""></button>\n        <button class="cg-th" type="button" data-full="__G_P4_3__"><img src="__G_P4_3__" alt=""></button>\n      </div></div>',
'p5':'<div class="cgallery"><img class="cg-main" src="__G_P5_1__" alt="Executive decision report"></div>',
'p6':'<div class="cgallery"><img class="cg-main" src="__G_P6_1__" alt="Accounting system">\n      <div class="cg-thumbs">\n        <button class="cg-th on" type="button" data-full="__G_P6_1__"><img src="__G_P6_1__" alt=""></button>\n        <button class="cg-th" type="button" data-full="__G_P6_2__"><img src="__G_P6_2__" alt=""></button>\n      </div></div>',
}
case_en=re.search(r'(<div id="case-data" hidden>.*?</div>)\n\n<div class="overlay"', ENOLD, re.S).group(1)
for pid,gal in GAL.items():
    case_en=case_en.replace(f'<div data-case="{pid}">\n    <span class="cat-tag">',
                            f'<div data-case="{pid}">\n    {gal}\n    <span class="cat-tag">')
EN_CASE_P7='''  <div data-case="p7">
    <div class="cgallery"><img class="cg-main" src="__G_P7_1__" alt="Today board in the elevator maintenance system">
      <div class="cg-thumbs">
        <button class="cg-th on" type="button" data-full="__G_P7_1__"><img src="__G_P7_1__" alt=""></button>
        <button class="cg-th" type="button" data-full="__G_P7_2__"><img src="__G_P7_2__" alt=""></button>
        <button class="cg-th" type="button" data-full="__G_P7_3__"><img src="__G_P7_3__" alt=""></button>
        <button class="cg-th" type="button" data-full="__G_P7_4__"><img src="__G_P7_4__" alt=""></button>
        <button class="cg-th" type="button" data-full="__G_P7_5__"><img src="__G_P7_5__" alt=""></button>
        <button class="cg-th" type="button" data-full="__G_P7_6__"><img src="__G_P7_6__" alt=""></button>
      </div></div>
    <span class="cat-tag">Full web operating system · two interfaces, one database</span>
    <h3>Elevator maintenance: the contract generates the work</h3>
    <p class="sector">An elevator maintenance company in Jeddah running a large fleet across dozens of clients and sites</p>
    <div class="part"><b>The problem</b><p>The whole operation ran on paper and WhatsApp: every client on a different maintenance cycle computed by hand and forgotten, technician reports lost in messages, contracts expiring unnoticed so maintenance kept running without one, and spare-part requests buried in chats never reaching the supplier.</p></div>
    <div class="part"><b>The system</b><p>The idea the whole system is built on: the contract is the engine. Its start date, end date and cycle auto-generate each month&#39;s tasks for every due elevator, and when it expires it turns red on every screen, its tasks stop, and the technician sees an alert to check with management. Two radically different interfaces: a 15-section admin panel for desktop, and a mobile field panel the technician enters with a single code and uses to log visits with photos and a 35-item inspection checklist. The official report reproduces the company&#39;s own approved paper form, auto-filled and print-ready.</p></div>
    <div class="part"><b>The result</b><p>One source of truth instead of paper and messages: a month&#39;s tasks generated in one click instead of manually computing dozens of different cycles, every visit documented with its time, photos and official report, contracts nearing expiry visible before it&#39;s too late, and spare-part requests organized per client with their status and supplier. The system runs on cloud plans whose current cost is zero and scales as the data grows.</p></div>
    <div class="kpis">
      <div class="kpi"><div class="v num">35</div><div class="l">inspection items on the approved form</div></div>
      <div class="kpi"><div class="v num">15</div><div class="l">admin sections plus 4 for the technician</div></div>
      <div class="kpi"><div class="v num">2</div><div class="l">interfaces: desktop admin and mobile field</div></div>
      <div class="kpi"><div class="v num">3</div><div class="l">roles enforced by the database itself</div></div>
    </div>
    <a class="ask" href="https://wa.me/966548767480?text=Hello%20Nawaf%2C%20I%27d%20like%20a%20similar%20operating%20system%20for%20my%20business" target="_blank" rel="noopener">I want a similar operating system</a>
    <p class="pd-note">All data visible in the screenshots is placeholder data; the client&#39;s identity is hidden at their request.</p>
  </div>
'''
case_en=case_en[:case_en.rfind('</div>')]+EN_CASE_P7+'</div>'
h=re.sub(r'<div id="case-data" hidden>.*?(<!-- بيانات الانظمة الجاهزة -->\n<div id="product-data")',
         lambda m: case_en+'\n\n\\g<1>', h, flags=re.S)
# fix the backref literal
h=h.replace('\\g<1>','<!-- ready systems -->\n<div id="product-data"')

# ---- 4) dict translate the rest ----
T={
# eyebrows
'<span class="eyebrow">اعمال مختارة</span>':'<span class="eyebrow">Selected Work</span>',
'<span class="eyebrow">الخدمات</span>':'<span class="eyebrow">Services</span>',
'<span class="eyebrow">الانظمة الجاهزة</span>':'<span class="eyebrow">Ready Systems</span>',
'<span class="eyebrow">شهادات موثقة</span>':'<span class="eyebrow">On the record</span>',
'<span class="eyebrow">كل الاعمال</span>':'<span class="eyebrow">All Work</span>',
# nav / brand / menu
'نواف الشريف<small>انظمة بيانات واتمتة اعمال</small>':'Nawaf Al-Shareif<small>Data Systems &amp; Automation</small>',
'>الاعمال</a>':'>Work</a>','>الارشيف الكامل</a>':'>Full archive</a>','>الارشيف</a>':'>Archive</a>',
'>الخدمات</a>':'>Services</a>','>الانظمة الجاهزة</a>':'>Ready Systems</a>','>عني</a>':'>About</a>','>تواصل</a>':'>Contact</a>',
'aria-label="القائمة"':'aria-label="Menu"','>اغلاق ✕</button>':'>Close ✕</button>',
# hero
'كل شيء عندك مسجل.':'Everything is recorded.','ولا شيء واضح.':'Nothing is clear.',
'مبيعات في ملف ومصاريف في ملف ثاني ومخزون في ثالث. والقرار المهم معلق ينتظر.':'Sales in one file, expenses in another, inventory in a third. And the decision that matters keeps waiting.',
'هنا يبدأ <span class="accent">النظام.</span>':'This is where the <span class="accent">system</span> begins.',
'انا نواف الشريف. محلل بيانات ومصمم انظمة اعمال. اجمع ارقامك في نظام واحد يظهر لك الصورة كاملة ويحسم قرارك.':'I&#39;m Nawaf Al-Shareif, data analyst and business systems designer. I bring your numbers into one system that shows the full picture and settles the decision.',
# metrics
'عملية بيع جمعتها في داشبورد واحد':'sales unified into a single dashboard',
'تقييم موثق 5/5 عبر 3 منصات':'documented 5/5 reviews across 3 platforms',
'نظام منفذ لعملاء حقيقيين':'systems delivered to real clients',
'قطاعات من المطاعم الى المقاولات':'sectors, from restaurants to contracting',
'ارقام من مشاريع حقيقية موثقة في ':'Real, verifiable numbers from documented projects on ',
' وخمسات ومنصات العمل الحر</p>':', Khamsat and freelance platforms</p>',
# work
'انظمة غيرت طريقة اتخاذ القرار':'Systems that changed how decisions get made',
'كل سطر مشروع حقيقي برقم حقيقي. اضغط على اي مشروع لتقرأ القصة كاملة.':'Every line is a real project with a real number. Click any of them to read the full story.',
'صيانة المصاعد: العقد يولّد العمل':'Elevator maintenance: the contract generates the work',
'بند فحص لكل زيارة صيانة':'inspection items per maintenance visit',
'مصنع منظفات في 6 فروع':'A cleaning-products factory, 6 branches',
'داشبورد مبيعات ومخزون</span>':'Sales &amp; inventory dashboard</span>',
'373 اقامة وجواز تحت المراقبة':'373 residency permits under watch',
'نظام انذار مبكر للاقامات':'Early-warning compliance system',
'مطعم ورقة: نظام تشغيل كامل':'Waraqa restaurant: a full operating system',
'منظومة ادارة وتشغيل':'Operations & management suite',
'الخبر: 18 وحدة او 33؟':'Al Khobar: 18 units or 33?',
'دراسة جدوى عقارية</span>':'Real-estate feasibility study</span>',
'شركة تقنية تسأل: نتوسع الان؟':'A SaaS company asks: expand now?',
'تقرير قرار تنفيذي</span>':'Executive decision report</span>',
'دورة محاسبية كاملة في ملف واحد':'A full accounting cycle in one file',
'نظام محاسبي على اكسل':'Excel accounting system',
'تصفح الارشيف الكامل: 22 مشروع':'Browse the full archive: 22 projects',
# services
'ماذا اقدم':'What I do',
'اربع خدمات هدفها واحد: قرار اوضح وعمل اخف.':'Four services, one goal: clearer decisions and lighter work.',
'انظمة التشغيل المخصصة':'Custom operating systems',
'نظام كامل يدير دورة عملك اليومية من الطلب الى التقرير: الطلبات والمخزون والعملاء والمحاسبة والرواتب وتقييم الاداء. يبنى على المنصة التي تناسب حجمك.':'A complete system that runs your daily cycle from order to report: orders, inventory, clients, accounting, payroll and performance. Built on the platform that fits your size.',
'اكسل بدون اشتراكات':'Excel, no subscriptions','قوقل شيتس لفريق متصل':'Google Sheets for connected teams','نظام ويب خاص للتوسع':'Custom web system for scale',
'المدة <i>حسب المنصة والنطاق باتفاق مسبق</i>':'Timeline <i>scoped and agreed upfront</i>',
'الداشبوردات وتحليل البيانات':'Dashboards & data analysis',
'داشبورد تفاعلي على اكسل او Power BI يجمع ارقامك المبعثرة في شاشة واحدة: المبيعات والمخزون واداء الفروع.':'An interactive Excel or Power BI dashboard that pulls your scattered numbers into one screen: sales, inventory, branch performance.',
'تنظيف البيانات قبل العرض':'Data cleaned before it&#39;s charted','مؤشرات على مقاس اسئلتك':'KPIs built around your questions','تحديث سهل':'Easy updates',
'المدة <i>من 3 الى 7 ايام</i>':'Timeline <i>3 to 7 days</i>',
'اتمتة الاعمال':'Business automation',
'المهام التي تكررها يدويًا كل اسبوع تتحول الى مسار يعمل وحده: تقارير دورية ومتابعات وتصنيف ورسائل.':'The tasks you repeat by hand every week become a flow that runs itself: recurring reports, follow-ups, classification, messages.',
'نبدأ بمهمة واحدة صغيرة':'We start with one small task','ثم نتوسع بما يثبت نفعه':'Then expand what proves useful',
'المدة <i>حسب النطاق</i>':'Timeline <i>depends on scope</i>',
'النماذج المالية ودراسات الجدوى':'Financial models & feasibility studies',
'دراسة او نموذج مالي بارقام واقعية: التكاليف والايرادات المتوقعة ونقطة التعادل وعائد الاستثمار. وتنتهي دائمًا بتوصية صريحة لان العميل لا يدفع مقابل جداول بل مقابل قرار.':'A study or model built on realistic numbers: costs, projected revenue, break-even point and return on investment. It always ends with an explicit recommendation, because clients don&#39;t pay for spreadsheets. They pay for a decision.',
'سيناريوهات متعددة':'Multiple scenarios','نقطة التعادل':'Break-even analysis','توصية مكتوبة صريحة':'A written, explicit recommendation',
'المدة <i>من 7 الى 14 يوم</i>':'Timeline <i>7 to 14 days</i>',
# products head
'انظمة جاهزة تستلمها اليوم':'Ready-made systems, delivered today',
'نفس جودة انظمة عملائي في ملفات جاهزة بسعر ثابت. تدفع مرة واحدة وتستلم فورًا مع ضمان استرجاع 14 يوم.':'The same quality as my client work, packaged at a fixed price. Pay once, receive instantly, with a 14-day money-back guarantee.',
# badges (cards + detail)
'>مجاني · بدون بطاقة</span>':'>Free · no card</span>','>مجاني</span>':'>Free</span>','>الاشمل</span>':'>Most complete</span>',
'>للتسعير</span>':'>For pricing</span>','>للالتزامات</span>':'>For commitments</span>','>بلغتين</span>':'>Bilingual</span>',
# product names
'حاسبة التسعير والربح':'Pricing & Profit Calculator','نظام ادارة المتجر':'Store Management System',
'>ربحي</h3>':'>Ribhi</h3>','>مسدد</h3>':'>Musaddad</h3>','ادارة الدخل والمصروفات':'Income & Expense Manager',
'نظام ربحي':'Ribhi','نظام مسدد':'Musaddad',
# card pd
'ملف اكسل للمشاريع الصغيرة يظهر لك هامش ربحك الحقيقي قبل ان تحدد اسعارك.':'An Excel file for small businesses that shows your real margin before you set prices.',
'دورة متجرك كاملة في ملف واحد: من تسجيل الطلب الى ملخص الضريبة.':'Your store&#39;s entire cycle in one file, from order entry to the VAT summary.',
'تدخل التكلفة فيظهر لك السعر المناسب فورًا مع سجل كامل لارباحك.':'Enter a cost and get the right price instantly, with a full record of your profits.',
'كل اقساطك والتزاماتك المالية في مكان واحد يظهر لك المدفوع والمتبقي.':'All your installments and financial commitments in one place: paid and remaining.',
'قالب بسيط يضبط دخلك ومصاريفك الشهرية بالعربية والانجليزية معًا.':'A simple template that keeps your monthly income and spending in order, in Arabic and English.',
# detail descriptions
'ملف اكسل مجاني للمشاريع الصغيرة يظهر لك هامش ربحك الحقيقي قبل ان تحدد اسعارك. تدخل تكاليفك وهامش الربح المستهدف فيحسب لك السعر المناسب لكل منتج ويوضح نقطة التعادل ويقيم اسعارك الحالية بالالوان.':'A free Excel file for small businesses that shows your real profit margin before you set prices. Enter your costs and target margin, and it computes the right price per product, shows the break-even point and color-rates your current prices.',
'دورة متجرك كاملة في ملف واحد من تسجيل الطلب الى ملخص الضريبة. يدير الطلبات والمنتجات وقاعدة العملاء ويصنفهم تلقائيًا ويعرض داشبورد باثني عشر مؤشرًا مع ملخص ضريبة القيمة المضافة ربع سنوي جاهز للتقديم.':'Your store&#39;s entire cycle in one file, from order entry to the VAT summary. It manages orders, products and the customer base, classifies customers automatically and shows a 12-metric dashboard with a quarterly VAT summary ready to file.',
'نظام تسعير وارباح متكامل. تدخل التكلفة فيظهر لك السعر المناسب فورًا ويحتفظ بسجل كامل لارباحك مع تتبع تكاليفك الشهرية الثابتة وداشبورد يعطيك توصيات عملية.':'A complete pricing-and-profit system. Enter a cost and get the right price instantly, with a full record of your profits, tracking of your fixed monthly costs and a dashboard that gives practical recommendations.',
'برنامج متابعة الاقساط الذكي. كل اقساطك والتزاماتك المالية في مكان واحد يظهر لك المدفوع والمتبقي مع داشبورد بالاجمالي والمتبقي وتحليل شهري وصفحة ملخص ودليل استخدام مفصل.':'A smart installment tracker. All your installments and financial commitments in one place, showing paid and remaining, with a totals-and-balances dashboard, monthly analysis, a summary page and a detailed usage guide.',
'قالب بسيط يضبط دخلك ومصاريفك الشهرية بالعربية والانجليزية معًا. سجل شهري حتى 2,000 عملية مع داشبورد برسوم توضح مصاريفك وتصنيفات قابلة للتخصيص ونسختان بلغتين بشراء واحد.':'A simple template that keeps your monthly income and spending in order, in Arabic and English. A monthly log up to 2,000 entries, a dashboard with clear spending charts, customizable categories and both language versions in one purchase.',
# detail sector lines
'ملف اكسل متكامل · تسليم فوري':'Integrated Excel file · instant delivery','ملف اكسل جاهز · تسليم فوري':'Excel file · instant delivery','قالب اكسل · نسختان بلغتين':'Excel template · two languages',
# feat / ul li
'حساب السعر تلقائيًا من هامش الربح المستهدف':'Auto price from your target margin','نقطة التعادل لكل منتج':'Break-even point per product',
'تقييم اسعارك الحالية بالالوان':'Color-coded rating of current prices','حتى 25 منتج':'Up to 25 products',
'حتى 2,000 طلب و300 منتج':'Up to 2,000 orders and 300 products','قاعدة عملاء بتصنيف تلقائي':'Customer base with auto classification',
'داشبورد بـ12 مؤشر':'Dashboard with 12 metrics','ملخص ضريبة القيمة المضافة ربع السنوي':'Quarterly VAT summary',
'حاسبة تسعير فورية':'Instant pricing calculator','حتى 1,000 منتج و5,000 طلب':'Up to 1,000 products and 5,000 orders',
'تكاليف شهرية ثابتة حتى 500 بند':'Fixed monthly costs, up to 500 items','داشبورد بتوصيات':'Dashboard with recommendations',
'حتى 1,000 التزام و3,000 دفعة':'Up to 1,000 commitments and 3,000 payments','داشبورد بالاجمالي والمتبقي':'Dashboard of totals and balances',
'تحليل شهري وصفحة ملخص':'Monthly analysis and summary page','دليل استخدام مفصل':'Detailed usage guide',
'سجل شهري حتى 2,000 عملية':'Monthly log, up to 2,000 entries','داشبورد برسوم توضح مصاريفك':'Dashboard with clear spending charts',
'تصنيفات قابلة للتخصيص':'Customizable categories','نسختان بلغتين بشراء واحد':'Both languages in one purchase',
# prices
'0 <i>بدون بطاقة</i>':'0 <i>no card needed</i>','349 <i>ريال · دفعة واحدة</i>':'349 <i>SAR · one-time</i>',
'289 <i>ريال · دفعة واحدة</i>':'289 <i>SAR · one-time</i>','179 <i>ريال · دفعة واحدة</i>':'179 <i>SAR · one-time</i>','99 <i>ريال · دفعة واحدة</i>':'99 <i>SAR · one-time</i>',
# order buttons + notes + wa msgs
'>ارسلها لي</a>':'>Send it to me</a>','>اطلبه الان</a>':'>Order it</a>',
'تسليم فوري على الواتساب.':'Delivered instantly on WhatsApp.','تسليم فوري بعد الشراء مع ضمان استرجاع 14 يوم.':'Delivered instantly after purchase, with a 14-day money-back guarantee.',
'مرحبا نواف، ابغى الحاسبة المجانية للتسعير والربح':'Hello Nawaf, I would like the free pricing and profit calculator',
'مرحبا نواف، ابغى اطلب نظام ادارة المتجر':'Hello Nawaf, I would like to order the Store Management System',
'مرحبا نواف، ابغى اطلب نظام ربحي':'Hello Nawaf, I would like to order Ribhi',
'مرحبا نواف، ابغى اطلب نظام مسدد':'Hello Nawaf, I would like to order Musaddad',
'مرحبا نواف، ابغى اطلب قالب الدخل والمصروفات':'Hello Nawaf, I would like to order the Income & Expense template',
'كل الانظمة تسلم فورًا بعد الشراء. اذا احتجت نظام على مقاسك بالضبط فهذا تخصصي الاساسي: ':'All systems are delivered instantly after purchase. Need one built exactly to your measure? That&#39;s my core work: ',
'>اطلب نظام مخصص</a>':'>request a custom system</a>',
# about
'المشكلة نادرًا ما تكون في الارقام نفسها. المشكلة في غياب <span class="accent">النظام</span> الذي يحولها الى قرارات.':'The problem is rarely the numbers themselves. It&#39;s the absence of a <span class="accent">system</span> that turns them into decisions.',
'بدأت من 2020 وانا اعمل على سؤال واحد يتكرر عند كل صاحب منشأة: ارقامي موجودة فلماذا لا استطيع ان اقرر؟':'Since 2020 I&#39;ve been working on the one question every business owner repeats: my numbers exist, so why can&#39;t I decide?',
'عملت داخل المنشآت قبل ان اعمل معها: اسست ادارات من الصفر وصممت انظمة تشغيل كاملة لمطاعم وشركات خدمات وقدت مشاريع تشخيص تشغيلي تكتشف مكان الاختناق قبل معالجته.':'I worked inside companies before working with them: founding departments from scratch, designing complete operating systems for restaurants and service companies, and leading operational diagnostics that find the bottleneck before treating it.',
'اليوم اعمل مستقلًا مع اصحاب المنشآت الصغيرة والمتوسطة في السعودية والخليج: مطاعم ومقاولات وتجزئة وعقار وقطاع صحي وخدمة عملاء.':'Today I work independently with SME owners across Saudi Arabia and the GCC: restaurants, contracting, retail, real estate, healthcare and customer service.',
'نواف الشريف · محلل بيانات ومصمم انظمة':'Nawaf Al-Shareif · data analyst & systems designer',
# principles
'التشخيص قبل التنفيذ':'Diagnosis before delivery',
'افهم المشكلة الحقيقية اولًا. كثير من الطلبات يتضح ان لها حل ابسط وارخص من المطلوب، واقولها لك بصراحة.':'I understand the real problem first. Many requests turn out to have a simpler, cheaper answer, and I&#39;ll tell you so plainly.',
'اتفاق بلا مفاجآت':'Agreements without surprises',
'نطاق محدد وسعر ثابت ومدة معلنة قبل البداية. لا مشاريع مفتوحة ولا تكاليف تظهر في المنتصف.':'Fixed scope, fixed price and a stated timeline before we start. No open-ended projects and no costs appearing midway.',
'تسليم يستخدم فعلًا':'Delivery that gets used',
'النظام يسلم جاهزًا للعمل مع شرح استخدامه لان النظام الذي لا يستخدم مجرد ملف اخر يضاف الى التبعثر.':'The system arrives working, with instructions. A system nobody uses is just one more file added to the clutter.',
# reviews
'كلام العملاء الموثق':'What clients say, on the record',
'36 تقييم بدرجة 5/5 عبر ثلاث منصات عمل حر. هذه عينة منها بنصها.':'36 five-star reviews across three freelance platforms. A sample, quoted as written.',
'«بدون مبالغة هذا الشخص افضل من تعاملت معهم عن بعد. جزاه الله خير»':'"Without exaggeration, the best person I&#39;ve worked with remotely."',
'عميل نظام حضور وانصراف · مستقل':'Attendance system client · Mostaql',
'«مبدع حرفيًا، انصح الجميع بالتعامل مع نواف»':'"Genuinely creative. I recommend working with Nawaf to everyone."',
'عميل داشبورد ذاتي التحديث · مستقل':'Self-updating dashboard client · Mostaql',
'«شخص محترف ومتعاون جدًا، سلم الشغل بجودة ممتازة»':'"Professional and very cooperative. Delivered excellent quality."',
'عميل موثق · خمسات':'Verified client · Khamsat',
'«افضل من اخرج لي البيانات، بشكل سريع ومتجاوب جدًا»':'"The best data extraction I&#39;ve had. Fast and very responsive."',
'عميل استخراج بيانات مالية · مستقل':'Financial data client · Mostaql',
'«محترف في الاعمال وسريع في الانجاز»':'"Professional in the work and fast to deliver."',
'عميل استراتيجية مبيعات · تواصل مباشر':'Sales strategy client · direct',
'«رائع بالتعامل وبالعمل»':'"Excellent to deal with and excellent work."',
'عميل حاسبة تكاليف مشاريع · خمسات':'Cost calculator client · Khamsat',
'«يعطيك العافية على العمل الذي قدمته»':'"Thank you for the quality of the work delivered."',
'عميل نظام محاسبة زراعية · مستقل':'Agricultural accounting client · Mostaql',
'<b class="num">12</b>تقييم في <a href="https://mostaql.com/u/EngNawaf" target="_blank" rel="noopener">مستقل</a>':'<b class="num">12</b>reviews on <a href="https://mostaql.com/u/EngNawaf" target="_blank" rel="noopener">Mostaql</a>',
'<b class="num">17</b>تقييم عبر تعاملات مباشرة موثقة من 6 سنوات':'<b class="num">17</b>reviews from direct dealings, verified over 6 years',
'<b class="num">7</b>تقييمات في خمسات بنسبة اكتمال 93%':'<b class="num">7</b>reviews on Khamsat, 93% completion rate',
# cta
'اجعل ارقامك تعمل لك <span class="accent">لا ضدك.</span>':'Make your numbers work for you, <span class="accent">not against you.</span>',
'ابدأ برسالة واحدة تشرح وضعك. اول قراءة للحالة بدون مقابل وبرأي صريح.':'Start with one message describing your situation. A first read of your case, free and with an honest verdict.',
'ابدأ الان <svg':'Start now <svg',
'<path d="M19 12H5"/><path d="m11 6-6 6 6 6"/>':'<path d="M5 12h14"/><path d="m13 6 6 6-6 6"/>',
# contact
'لديك قرار معلق على ارقام مبعثرة؟ <span class="accent">ارسلها لي.</span>':'A decision stuck on scattered numbers? <span class="accent">Send it over.</span>',
'اكتب وضعك كما هو بدون ترتيب. اول قراءة للحالة بدون تكلفة وبرأي صريح: تحتاج نظام او يكفيك حل ابسط.':'Describe your situation as it is, in any order. The first read is free, with an honest verdict: it needs a system, or something simpler will do.',
'او مباشرة:':'Or directly:','واتساب <span class="num">':'WhatsApp <span class="num">',
'>الاسم</label>':'>Name</label>','aria-label="اغلاق"':'aria-label="Close"','اسمك الكريم':'Your name','>نوع النشاط</label>':'>Type of business</label>',
'مطعم او متجر او مقاولات او غيره':'Restaurant, store, contracting, or other','>اوصف وضعك الحالي</label>':'>Describe your current situation</label>',
'مثال: لدي 3 فروع وكل فرع يسجل مبيعاته في ملف مختلف ولا اعرف ايها يربح':'Example: I run 3 branches, each logs sales in a different file, and I don&#39;t know which one makes money',
'اكتب بطريقتك. انا من يرتب.':'Write it your way. Organizing it is my job.','ارسل عبر واتساب':'Send via WhatsApp',
'الرسالة تفتح في واتسابك جاهزة بالتفاصيل وانت ترسلها بنفسك.':'The message opens in your WhatsApp, pre-filled. You send it yourself.',
# archive head + filters
'الارشيف الكامل: <span class="accent num">22</span> نظام موثق':'The full archive: <span class="accent num">22</span> documented systems',
'كل مشروع نفذ لعميل حقيقي او منشأة حقيقية. افتح اي سطر لتقرأ المشكلة والنظام والنتيجة.':'Every project was delivered to a real client or organization. Open any line to read the problem, the system and the result.',
'>الكل</button>':'>All</button>','>داشبوردات وتحليلات</button>':'>Dashboards & analytics</button>','>انظمة تشغيل</button>':'>Operations systems</button>',
'>تقارير تنفيذية</button>':'>Executive reports</button>','>دراسات جدوى ونماذج</button>':'>Feasibility & models</button>','>اتمتة وادوات</button>':'>Automation & tools</button>',
# gallery alts (case + product)
'اضغط في اي مكان للاغلاق':'Click anywhere to close','داشبورد المبيعات والمخزون':'Sales & inventory dashboard','لوحة مراقبة الاقامات':'Permits monitoring dashboard',
'دراسة الجدوى العقارية':'Feasibility study','تقرير القرار التنفيذي':'Executive decision report','النظام المحاسبي':'Accounting system',

# --- work cards (v9) ---
'نظام ادارة صيانة المصاعد':'Elevator Maintenance Management System',
'واجهتان في منظومة واحدة: ادارة على الحاسب وميدان على الجوال، والعقد يولّد مهام الصيانة تلقائيًا ويوقفها عند انتهائه.':'Two interfaces in one system: admin on desktop, field on mobile, with the contract auto-generating maintenance tasks and stopping them when it expires.',
'داشبورد المبيعات والمخزون لمصنع منظفات':'Sales &amp; Inventory Dashboard for a Cleaning-Products Factory',
'6 فروع في شاشة قرار واحدة على Power BI بعد ان كانت موزعة على 9 ملفات منفصلة.':'Six branches on one Power BI decision screen, after living in nine separate files.',
'نظام متابعة الاقامات والجوازات':'Residency &amp; Passport Compliance System',
'داشبورد استباقي يصنف الاقامات حسب قرب انتهائها ويكشف المنتهية قبل ان تتحول الى غرامات.':'A proactive dashboard that classifies permits by how close they are to expiry and surfaces expired ones before they become fines.',
'نظام تشغيل مطعم متكامل':'Complete Restaurant Operations System',
'8 اقسام مترابطة تغطي المالية والعمليات والرواتب ومنصات التوصيل، مع خطة نمو 60 يوم.':'Eight interconnected divisions covering finance, operations, payroll and delivery platforms, with a 60-day growth plan.',
'دراسة جدوى شقق فندقية في الخبر':'Serviced-Apartments Feasibility Study, Al Khobar',
'مقارنة مالية كاملة بين تصميمين بايراداتهما وفترة الاسترداد، وتوصية صريحة بالاعلى عائدًا.':'A full financial comparison of two designs with revenue and payback period, ending in an explicit recommendation for the higher return.',
'تقرير قرار: هل نتوسع اقليميًا الان؟':'Decision Report: Expand Regionally Now?',
'قراءة مؤشرات النمو وتركز الايراد وتكلفة اكتساب العميل، تنتهي بتوصية نهائية مكتوبة.':'A reading of growth, revenue concentration and customer acquisition cost, ending in a written final recommendation.',
'نظام محاسبي كامل على اكسل':'Complete Excel Accounting System',
'22 ورقة مترابطة تغطي الدورة من القيد الاول الى القوائم المالية بدون اي اشتراكات.':'22 interconnected sheets covering the cycle from the first entry to the financial statements, with no subscriptions.',
'>نظام ويب</span>':'>Web system</span>',
'>داشبورد</span>':'>Dashboard</span>',
'>نظام انذار مبكر</span>':'>Early-warning system</span>',
'>نظام تشغيل</span>':'>Operations system</span>',
'>دراسة جدوى</span>':'>Feasibility study</span>',
'>تقرير تنفيذي</span>':'>Executive report</span>',
'>نظام محاسبي</span>':'>Accounting system</span>',
'<small>بند فحص</small>':'<small>inspection items</small>',
'<small>عملية بيع</small>':'<small>sales</small>',
'<small>اقامة منتهية</small>':'<small>expired permits</small>',
'<small>ملف تشغيلي</small>':'<small>operational files</small>',
'<small>زيادة الوحدات</small>':'<small>more units</small>',
'<small>من الايراد محلي</small>':'<small>revenue domestic</small>',
'<small>ورقة مترابطة</small>':'<small>linked sheets</small>',
'التفاصيل والصور <svg':'View details <svg',
'aria-label="السابق"':'aria-label="Previous"',
'aria-label="التالي"':'aria-label="Next"',
# stragglers
'>مستقل</a>':'>Mostaql</a>',
'نواف الشريف · انظمة بيانات واتمتة اعمال · منذ 2020':'Nawaf Al-Shareif · Data systems & business automation · Since 2020',
}
# apply longest keys first so short keys never clobber longer phrases
for a in sorted(T, key=len, reverse=True):
    h=h.replace(a,T[a])

open(os.path.join(HERE,'artifact-en.html'),'w',encoding='utf-8').write(h)
# report leftover Arabic (excluding wa.me encoded and lang toggles العربية/عربي)
import re as _re
ar_left=_re.findall(r'>[^<>]*[؀-ۿ][^<>]*<', h)
ar_left=[x for x in ar_left if 'العربية' not in x and 'عربي' not in x]
print('leftover arabic text nodes:', len(ar_left))
for x in ar_left[:40]: print('  ', x[:90])
