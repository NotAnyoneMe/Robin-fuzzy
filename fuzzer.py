import requests
import threading
from queue import Queue
from urllib.parse import urljoin
import sys
import time
from typing import Set
from colorama import Fore, Back, Style, init
import argparse

init(autoreset=True)

class WebFuzzer:
    def __init__(self, target: str, wordlist_path: str = "paths.txt", threads: int = 20, debug: bool = False):
        self.target = target.rstrip('/')
        self.wordlist_path = wordlist_path
        self.threads = threads
        self.debug = debug
        self.q = Queue()
        self.found_urls: Set[str] = set()
        self.lock = threading.Lock()
        self.total_paths = 0
        self.scanned = 0
        self.errors = 0
        
    def print_banner(self):
        """Display the banner"""
        banner = f"""
{Fore.CYAN}╦═╗╔═╗╔╗ ╦╔╗╔  ╔═╗╦ ╦╔═╗╔═╗╦ ╦
{Fore.CYAN}╠╦╝║ ║╠╩╗║║║║  ╠╣ ║ ║╔═╝╔═╝╚╦╝
{Fore.CYAN}╩╚═╚═╝╚═╝╩╝╚╝  ╚  ╚═╝╚═╝╚═╝ ╩ 
{Style.BRIGHT}{Fore.YELLOW}═══════════════════════════════════════
{Fore.GREEN}    Web Directory Fuzzing Tool v2.0
{Fore.YELLOW}═══════════════════════════════════════
{Fore.MAGENTA}    Telegram: {Fore.WHITE}@MLBOR
{Fore.MAGENTA}    Github:   {Fore.WHITE}NotAnyOneMe
{Fore.YELLOW}═══════════════════════════════════════{Style.RESET_ALL}
"""
        print(banner)
        
    def debug_log(self, message: str, level: str = "INFO"):
        """Print debug messages if debug mode is enabled"""
        if self.debug:
            timestamp = time.strftime("%H:%M:%S")
            colors = {
                "INFO": Fore.CYAN,
                "SUCCESS": Fore.GREEN,
                "WARNING": Fore.YELLOW,
                "ERROR": Fore.RED,
                "DEBUG": Fore.MAGENTA
            }
            color = colors.get(level, Fore.WHITE)
            print(f"{Fore.WHITE}[{timestamp}] {color}[{level}]{Style.RESET_ALL} {message}")
    
    def load_wordlist(self):
        """Load paths from wordlist file"""
        try:
            self.debug_log(f"Opening wordlist file: {self.wordlist_path}", "DEBUG")
            with open(self.wordlist_path, 'r', encoding='utf-8', errors='ignore') as f:
                paths = [line.strip() for line in f if line.strip() and not line.startswith('#')]
            self.debug_log(f"Successfully loaded {len(paths)} paths", "SUCCESS")
            return paths
        except FileNotFoundError:
            print(f"{Fore.RED}[!] Error: Wordlist file '{self.wordlist_path}' not found{Style.RESET_ALL}")
            sys.exit(1)
        except Exception as e:
            print(f"{Fore.RED}[!] Error reading wordlist: {e}{Style.RESET_ALL}")
            sys.exit(1)
    
    def normalize_path(self, path: str) -> str:
        """Ensure path starts with /"""
        if not path.startswith('/'):
            path = '/' + path
        return path
    
    def worker(self):
        """Worker thread to process URLs from queue"""
        session = requests.Session()
        session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        
        thread_id = threading.current_thread().name
        self.debug_log(f"Worker thread {thread_id} started", "DEBUG")
        
        while not self.q.empty():
            try:
                path = self.q.get(timeout=1)
                url = urljoin(self.target + '/', path.lstrip('/'))
                
                self.debug_log(f"Testing: {url}", "DEBUG")
                
                try:
                    response = session.get(
                        url,
                        timeout=5,
                        allow_redirects=False,
                        verify=False
                    )
                    
                    status = response.status_code
                    
                    # Check for interesting status codes
                    if status in [200, 201, 204, 301, 302, 307, 308, 401, 403, 405, 500]:
                        size = len(response.content)
                        
                        with self.lock:
                            if url not in self.found_urls:
                                self.found_urls.add(url)
                                status_msg = self._format_result(status, size, url)
                                print(status_msg)
                                
                                self.debug_log(f"Found interesting path: {path} (Status: {status})", "SUCCESS")
                
                except requests.exceptions.Timeout:
                    self.debug_log(f"Timeout: {url}", "WARNING")
                    with self.lock:
                        self.errors += 1
                except requests.exceptions.ConnectionError:
                    self.debug_log(f"Connection error: {url}", "ERROR")
                    with self.lock:
                        self.errors += 1
                except Exception as e:
                    self.debug_log(f"Exception for {url}: {str(e)}", "ERROR")
                    with self.lock:
                        self.errors += 1
                
                with self.lock:
                    self.scanned += 1
                    if self.scanned % 100 == 0 or self.debug:
                        progress = (self.scanned / self.total_paths) * 100
                        prog_bar = self._create_progress_bar(progress)
                        print(f"\r{Fore.CYAN}[*] Progress: {prog_bar} {self.scanned}/{self.total_paths} ({progress:.1f}%){Style.RESET_ALL}", end='')
                
                self.q.task_done()
                
            except:
                break
        
        self.debug_log(f"Worker thread {thread_id} finished", "DEBUG")
    
    def _create_progress_bar(self, percentage: float, length: int = 30) -> str:
        """Create a visual progress bar"""
        filled = int(length * percentage / 100)
        bar = '█' * filled + '░' * (length - filled)
        return f"{Fore.GREEN}{bar}{Style.RESET_ALL}"
    
    def _format_result(self, status: int, size: int, url: str) -> str:
        """Format the result output with colors"""
        status_color = self._get_status_color(status)
        status_text = f"{status_color}[{status}]{Style.RESET_ALL}"
        
        size_color = Fore.WHITE
        if size > 10000:
            size_color = Fore.YELLOW
        if size > 100000:
            size_color = Fore.RED
            
        return f"{status_text} {Fore.CYAN}[Size: {size_color}{size:>7}{Fore.CYAN}]{Style.RESET_ALL} {Fore.WHITE}{url}{Style.RESET_ALL}"
    
    def _get_status_color(self, status: int) -> str:
        """Get color code for status"""
        if status == 200:
            return Fore.GREEN
        elif status in [301, 302, 307, 308]:
            return Fore.BLUE
        elif status in [401, 403]:
            return Fore.YELLOW
        elif status >= 500:
            return Fore.RED
        else:
            return Fore.CYAN
    
    def start(self):
        """Start the fuzzing process"""
        self.print_banner()
        
        print(f"{Fore.YELLOW}[*]{Style.RESET_ALL} Target:   {Fore.WHITE}{self.target}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}[*]{Style.RESET_ALL} Wordlist: {Fore.WHITE}{self.wordlist_path}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}[*]{Style.RESET_ALL} Threads:  {Fore.WHITE}{self.threads}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}[*]{Style.RESET_ALL} Debug:    {Fore.WHITE}{self.debug}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}[*]{Style.RESET_ALL} Loading wordlist...")
        
        # Load wordlist
        paths = self.load_wordlist()
        self.total_paths = len(paths)
        print(f"{Fore.GREEN}[+]{Style.RESET_ALL} Loaded {Fore.WHITE}{self.total_paths}{Style.RESET_ALL} paths")
        
        # Add paths to queue
        for path in paths:
            self.q.put(self.normalize_path(path))
        
        print(f"\n{Fore.GREEN}[*] Starting scan...{Style.RESET_ALL}\n")
        start_time = time.time()
        
        # Disable SSL warnings
        requests.packages.urllib3.disable_warnings()
        
        # Start threads
        threads = []
        for i in range(self.threads):
            t = threading.Thread(target=self.worker, name=f"Worker-{i+1}")
            t.daemon = True
            t.start()
            threads.append(t)
            self.debug_log(f"Started thread {i+1}/{self.threads}", "DEBUG")
        
        # Wait for completion
        self.q.join()
        
        # Wait for threads to finish
        for t in threads:
            t.join(timeout=1)
        
        elapsed = time.time() - start_time
        
        print(f"\n\n{Fore.GREEN}{'═' * 50}{Style.RESET_ALL}")
        print(f"{Fore.GREEN}[+] Scan completed!{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}{'═' * 50}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}[*]{Style.RESET_ALL} Time elapsed:     {Fore.WHITE}{elapsed:.2f}s{Style.RESET_ALL}")
        print(f"{Fore.CYAN}[*]{Style.RESET_ALL} Paths found:      {Fore.GREEN}{len(self.found_urls)}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}[*]{Style.RESET_ALL} Total scanned:    {Fore.WHITE}{self.total_paths}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}[*]{Style.RESET_ALL} Request rate:     {Fore.WHITE}{self.total_paths/elapsed:.1f} req/s{Style.RESET_ALL}")
        if self.debug:
            print(f"{Fore.CYAN}[*]{Style.RESET_ALL} Errors:           {Fore.RED}{self.errors}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}{'═' * 50}{Style.RESET_ALL}\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Robin Fuzzy - Web Directory Fuzzing Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=f"""
{Fore.CYAN}Examples:{Style.RESET_ALL}
  python fuzzer.py -u https://example.com
  python fuzzer.py -u https://example.com -w paths.txt -t 30
  python fuzzer.py -u https://example.com -w paths.txt -t 50 --debug

{Fore.MAGENTA}Credits:{Style.RESET_ALL}
  Telegram: @MLBOR
  Github:   NotAnyOneMe
        """
    )
    
    parser.add_argument('-u', '--url', required=True, help='Target URL')
    parser.add_argument('-w', '--wordlist', default='paths.txt', help='Path to wordlist file (default: paths.txt)')
    parser.add_argument('-t', '--threads', type=int, default=20, help='Number of threads (default: 20)')
    parser.add_argument('-d', '--debug', action='store_true', help='Enable debug mode')
    
    args = parser.parse_args()
    
    fuzzer = WebFuzzer(args.url, args.wordlist, args.threads, args.debug)
    
    try:
        fuzzer.start()
    except KeyboardInterrupt:
        print(f"\n\n{Fore.RED}[!] Scan interrupted by user{Style.RESET_ALL}")
        sys.exit(0)
    except Exception as e:
        print(f"\n{Fore.RED}[!] Fatal error: {e}{Style.RESET_ALL}")
        sys.exit(1)
