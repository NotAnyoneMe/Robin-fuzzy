# 🦅 Robin Fuzzy

<div align="center">

```
╦═╗╔═╗╔╗ ╦╔╗╔  ╔═╗╦ ╦╔═╗╔═╗╦ ╦
╠╦╝║ ║╠╩╗║║║║  ╠╣ ║ ║╔═╝╔═╝╚╦╝
╩╚═╚═╝╚═╝╩╝╚╝  ╚  ╚═╝╚═╝╚═╝ ╩ 
```

**A Fast & Colorful Web Directory Fuzzing Tool**

[![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

</div>

---

## 📋 Description

Robin Fuzzy is a powerful, multi-threaded web directory and file fuzzing tool designed for penetration testing and security assessments. With beautiful colorized output and debug capabilities, it helps security professionals discover hidden paths, backup files, admin panels, and sensitive directories on web applications.

## ✨ Features

- 🚀 **Multi-threaded** - Fast scanning with configurable thread count
- 🎨 **Colorized Output** - Beautiful terminal colors using Colorama
- 🐛 **Debug Mode** - Detailed logging for troubleshooting
- 📊 **Progress Tracking** - Real-time progress bar and statistics
- 🎯 **Smart Detection** - Identifies interesting status codes (200, 301, 302, 403, 401, 500)
- 📈 **Performance Metrics** - Request rate and timing statistics
- 🔍 **Comprehensive Wordlist** - Includes 250+ common paths
- ⚡ **Session Reuse** - Efficient HTTP connection handling

## 🛠️ Installation

### Requirements

- Python 3.7 or higher
- pip (Python package manager)

### Install Dependencies

```bash
pip install requests colorama
```

### Clone Repository

```bash
git clone https://github.com/NotAnyOneMe/robin-fuzzy.git
cd robin-fuzzy
```

## 🚀 Usage

### Basic Scan

```bash
python fuzzer.py -u https://example.com
```

### Custom Wordlist and Threads

```bash
python fuzzer.py -u https://example.com -w custom_paths.txt -t 30
```

### Enable Debug Mode

```bash
python fuzzer.py -u https://example.com -w paths.txt -t 50 --debug
```

### Command Line Options

```
-u, --url         Target URL (required)
-w, --wordlist    Path to wordlist file (default: paths.txt)
-t, --threads     Number of threads (default: 20)
-d, --debug       Enable debug mode
-h, --help        Show help message
```

## 📝 Examples

**Scan with default settings:**
```bash
python fuzzer.py -u https://target.com
```

**Fast scan with 50 threads:**
```bash
python fuzzer.py -u https://target.com -t 50
```

**Debug mode for troubleshooting:**
```bash
python fuzzer.py -u https://target.com -w paths.txt --debug
```

**Custom wordlist:**
```bash
python fuzzer.py -u https://target.com -w /path/to/wordlist.txt -t 40
```

## 🎨 Output Colors

- 🟢 **Green** - 200 OK (Success)
- 🔵 **Blue** - 301/302/307/308 (Redirects)
- 🟡 **Yellow** - 401/403 (Authentication/Forbidden)
- 🔴 **Red** - 500+ (Server Errors)
- 🔷 **Cyan** - Other interesting status codes

## 📂 Project Structure

```
robin-fuzzy/
├── fuzzer.py          # Main fuzzing script
├── paths.txt          # Default wordlist (250+ paths)
├── README.md          # This file
└── LICENSE            # License file
```

## 🎯 Wordlist Categories

The included `paths.txt` covers:

- Admin panels & login pages
- API endpoints (REST, GraphQL)
- Backup files & databases
- Configuration files
- Upload directories
- CMS paths (WordPress, Joomla)
- Development/testing environments
- Database management tools
- E-commerce paths
- Security files
- And much more!

## ⚠️ Legal Disclaimer

**IMPORTANT:** This tool is designed for legal security testing and educational purposes only. 

- ✅ Only use on systems you own or have explicit permission to test
- ✅ Obtain written authorization before testing
- ✅ Comply with all applicable laws and regulations
- ❌ Unauthorized access to computer systems is illegal

The authors are not responsible for misuse or damage caused by this tool. Users are solely responsible for their actions.

## 🔒 Responsible Disclosure

If you discover vulnerabilities using this tool:

1. Report them responsibly to the affected organization
2. Do not exploit or share vulnerabilities publicly
3. Give organizations reasonable time to fix issues
4. Follow coordinated disclosure practices

## 🤝 Contributing

Contributions are welcome! Feel free to:

- Report bugs
- Suggest new features
- Submit pull requests
- Improve documentation
- Add more wordlists

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Credits

**Created by:**
- **Telegram:** [@MLBOR](https://t.me/MLBOR)
- **Github:** [NotAnyOneMe](https://github.com/NotAnyOneMe)

## 🌟 Support

If you find this tool useful, please:
- ⭐ Star this repository
- 🐛 Report issues
- 💡 Suggest improvements
- 📢 Share with others

## 📞 Contact

- **Telegram:** [@MLBOR](https://t.me/MLBOR)
- **GitHub:** [Issues](https://github.com/NotAnyOneMe/robin-fuzzy/issues)

---

<div align="center">

**Made with ❤️ for the Security Community**

*Happy Fuzzing! 🦅*

</div>
