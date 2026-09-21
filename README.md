# Repo Health

A small, dependency-free Python tool for auditing the practical health of a local source repository. Repo Health checks repository hygiene, baseline documentation, CI presence, unfinished-code markers, potentially sensitive files, and a few high-confidence credential patterns without executing the inspected project or uploading its contents.

**Author:** Radwan Abdulhadi Ahmed · رضوان عبدالهادي أحمد · [@rad03i2](https://github.com/rad03i2)

## English

### Why it exists
Repositories often become harder to share or maintain because basic project files are missing, unfinished markers accumulate, CI is absent, or a sensitive file slips into the tree. Repo Health provides a fast, deterministic local audit suitable for developers and CI pipelines.

### Key features
- Health score from 0–100 with error, warning, and informational findings.
- Checks for `README.md`, `LICENSE`, `.gitignore`, `SECURITY.md`, `CONTRIBUTING.md`, and GitHub Actions presence.
- Finds TODO/FIXME/HACK markers in common source-code extensions.
- Flags `.env` and common private-key/container file extensions for review.
- Detects a deliberately small set of high-confidence credential signatures without printing matched values.
- Skips common generated/vendor directories, symbolic links, binary-looking files, and files larger than 1 MB.
- Human-readable and JSON output.
- CI-friendly `--fail-on` and `--min-score` policies.
- Reusable Python API; no runtime dependencies.
- Read-only and offline: inspected files are never executed, changed, or uploaded.

### Requirements
Python 3.10 or newer.

### Installation
```bash
git clone https://github.com/rad03i2/repo-health.git
cd repo-health
python -m pip install -e .
```

### Usage
Audit the current repository:
```bash
repo-health .
```

Machine-readable output:
```bash
repo-health . --json
```

Fail CI on warnings or errors:
```bash
repo-health . --fail-on warning
```

Require a minimum score while ignoring severity-based failure:
```bash
repo-health . --fail-on never --min-score 85
```

Exit codes are `0` for an accepted audit, `1` when the configured quality gate fails, and `2` for invalid/unreadable input. The default policy fails only when an error-level finding exists.

### Python API
```python
from repo_health import audit

report = audit(".")
print(report.score)
for finding in report.findings:
    print(finding.severity, finding.code, finding.path)
```

### Configuration
Repo Health intentionally has no configuration file in v1. Policies are explicit CLI options so CI behavior is visible in workflow definitions. `--fail-on` accepts `never`, `warning`, or `error`; `--min-score` accepts 0–100.

### Preview guidance
For a portfolio screenshot, run `repo-health .` in a clean terminal at the repository root. The concise score, counts, and findings make a useful terminal preview without requiring a GUI.

### Project structure
```text
repo-health/
├── .github/workflows/ci.yml
├── src/repo_health/
│   ├── __init__.py
│   ├── cli.py
│   └── core.py
├── tests/
│   ├── test_cli.py
│   └── test_core.py
├── CONTRIBUTING.md
├── SECURITY.md
├── LICENSE
├── pyproject.toml
└── README.md
```

### Testing
```bash
python -m pip install -e .
python -m unittest discover -s tests -v
python -m compileall -q src
```
GitHub Actions runs the suite on Ubuntu, Windows, and macOS with Python 3.10, 3.12, and 3.13.

### Security and privacy
Audits are local and read-only. Repo Health never executes repository code and has no network or telemetry feature. Secret detection is heuristic and intentionally limited: a finding can be a false positive, and absence of a finding does **not** prove a repository contains no secrets. If a real credential has been committed, rotate it immediately; deleting the working-tree file alone does not remove it from Git history. See [SECURITY.md](SECURITY.md).

### Limitations
- This is a focused hygiene auditor, not a compiler, linter, dependency vulnerability scanner, malware scanner, or full secret-scanning product.
- Secret signatures are intentionally few to keep results understandable and reduce accidental exposure.
- Files over 1 MB, symlinks, binary-looking content, generated/vendor directories, and non-UTF-8 text are skipped.
- The score is a transparent convenience metric, not an objective measure of software quality.
- CI detection currently targets `.github/workflows`.

### Optional roadmap
Potential future additions include configurable policies, SARIF output, more repository hosts, and opt-in language-specific checks. These are not required for the current tool to work.

### Contributing
See [CONTRIBUTING.md](CONTRIBUTING.md). Keep checks deterministic, local, low-noise, and covered by tests.

### License
MIT License — see [LICENSE](LICENSE).

### Author
**Radwan Abdulhadi Ahmed**  
**رضوان عبدالهادي أحمد**  
GitHub: **[@rad03i2](https://github.com/rad03i2)**

---

## العربية

### نظرة عامة
**Repo Health** أداة بايثون خفيفة تعمل محليًا لفحص الحالة العملية لمستودع برمجي. تتحقق من نظافة بنية المشروع، ووجود ملفات التوثيق الأساسية، ووجود CI، وعلامات العمل غير المكتمل، وبعض الملفات أو الأنماط الحساسة، من دون تشغيل كود المشروع المفحوص أو رفع محتوياته إلى أي خدمة.

### لماذا أُنشئت؟
قد يصبح المستودع صعب المشاركة أو الصيانة بسبب غياب README أو الترخيص، أو تراكم TODO/FIXME، أو عدم وجود اختبارات آلية، أو دخول ملف حساس بالخطأ. توفر الأداة فحصًا سريعًا وحتميًا يصلح للاستخدام اليدوي وضمن CI.

### أهم الميزات
- درجة صحة من 0 إلى 100 مع نتائج بمستويات خطأ وتحذير ومعلومة.
- فحص `README.md` و`LICENSE` و`.gitignore` و`SECURITY.md` و`CONTRIBUTING.md` وGitHub Actions.
- كشف TODO/FIXME/HACK في امتدادات الشيفرة الشائعة.
- التنبيه إلى `.env` وامتدادات المفاتيح/الحاويات الحساسة الشائعة لمراجعتها.
- كشف مجموعة صغيرة ومقصودة من بصمات بيانات الاعتماد عالية الثقة من دون طباعة القيمة المطابقة.
- تجاهل مجلدات البناء والحزم الشائعة والروابط الرمزية والملفات الثنائية الظاهرة والملفات الأكبر من 1 MB.
- إخراج نصي أو JSON.
- بوابات جودة مناسبة لـCI عبر `--fail-on` و`--min-score`.
- API بايثون قابلة لإعادة الاستخدام ومن دون اعتماديات تشغيل خارجية.
- عمل محلي للقراءة فقط؛ لا تعديل ولا تنفيذ ولا رفع للملفات.

### المتطلبات والتثبيت
يتطلب Python 3.10 أو أحدث.
```bash
git clone https://github.com/rad03i2/repo-health.git
cd repo-health
python -m pip install -e .
```

### الاستخدام
```bash
repo-health .
repo-health . --json
repo-health . --fail-on warning
repo-health . --fail-on never --min-score 85
```
رمز الخروج `0` يعني قبول الفحص، و`1` يعني فشل بوابة الجودة المحددة، و`2` يعني مدخلًا غير صالح أو غير قابل للقراءة. افتراضيًا يفشل الأمر فقط عند وجود نتيجة بمستوى خطأ.

### API بايثون
```python
from repo_health import audit

report = audit(".")
print(report.score)
```

### الإعداد
لا يوجد ملف إعداد في الإصدار الأول عمدًا؛ سياسات CI تظهر صراحة في سطر الأوامر. يقبل `--fail-on` القيم `never` و`warning` و`error`، بينما يقبل `--min-score` رقمًا من 0 إلى 100.

### إرشاد المعاينة
لصورة مناسبة للـPortfolio، شغّل `repo-health .` من جذر المشروع في طرفية نظيفة. تظهر الدرجة وعدد الملفات والنتائج بصورة مختصرة ولا تحتاج الأداة إلى واجهة رسومية.

### بنية المشروع
الكود داخل `src/repo_health`، والاختبارات داخل `tests`، وسير CI في `.github/workflows/ci.yml`، مع ملفات الأمان والمساهمة والترخيص في جذر المستودع.

### الاختبارات
```bash
python -m pip install -e .
python -m unittest discover -s tests -v
python -m compileall -q src
```
ويشغّل GitHub Actions الاختبارات على Ubuntu وWindows وmacOS مع Python 3.10 و3.12 و3.13.

### الخصوصية والأمان
الفحص محلي وللقراءة فقط، ولا تشغّل الأداة شيفرة المستودع ولا تتصل بالشبكة ولا تحتوي Telemetry. كشف الأسرار استدلالي ومحدود؛ وجود تنبيه لا يثبت أن القيمة صالحة، وعدم وجود تنبيه لا يثبت خلو المستودع من الأسرار. إذا تم رفع اعتماد حقيقي إلى Git، فيجب إلغاؤه/تدويره ومعالجة تاريخه، وليس حذف الملف الحالي فقط. راجع [SECURITY.md](SECURITY.md).

### القيود
- ليست بديلًا عن compiler أو linter أو ماسح ثغرات الاعتماديات أو malware scanner أو secret scanner متكامل.
- أنماط الأسرار محدودة عمدًا لتقليل الضجيج وعدم إظهار القيم.
- يتم تجاوز الملفات الأكبر من 1 MB والروابط الرمزية والمحتوى الثنائي الظاهر والنص غير UTF-8 ومجلدات vendor/build الشائعة.
- الدرجة مؤشر عملي شفاف وليست قياسًا موضوعيًا لجودة البرنامج.
- كشف CI حاليًا مخصص لـ`.github/workflows`.

### تطوير اختياري
يمكن مستقبلًا إضافة سياسات قابلة للتخصيص وSARIF ودعم منصات مستودعات أخرى وفحوص لغات اختيارية. هذه إضافات مستقبلية وليست وظائف ناقصة من الغرض الحالي.

### المساهمة والترخيص
راجع [CONTRIBUTING.md](CONTRIBUTING.md) للمساهمة. المشروع مرخص وفق MIT؛ راجع [LICENSE](LICENSE).

### المؤلف
**Radwan Abdulhadi Ahmed**  
**رضوان عبدالهادي أحمد**  
GitHub: **[@rad03i2](https://github.com/rad03i2)**
