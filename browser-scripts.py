import argparse
from urllib.parse import urlparse, urljoin
import urllib.parse
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait           # \
from selenium.webdriver.support import expected_conditions as EC  # 
from webdriver_manager.chrome import ChromeDriverManager
import time
from har_exporter import HAR_Exporter
from selenium.common.exceptions import TimeoutException, NoSuchElementException




# ——————————————
# Helper: load domains.txt into a dict
# ——————————————
def load_domains(path="domains.txt"):
    domains = {}
    current = None
    with open(path, "r") as f:
        for raw in f:
            line = raw.strip()
            if not line or line.lower().startswith("list of"):
                continue
            if "." not in line:
                current = line
                domains[current] = []
            else:
                domains[current].append("https://" + line)
    return domains

# ——————————————
# Main
# ——————————————
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Browse domains and export a HAR per category.")
    parser.add_argument("--browser", choices=["chrome", "firefox"],
                        required=True, help="Which browser to run")
    args = parser.parse_args()

    print(f"Browser: {args.browser}")
    domains = load_domains()

    for category, sites in domains.items():
        if not sites:
            continue
        print(f"\n=== CATEGORY: {category} ===")

        # new exporter per category = new profile+HAR
        driver = HAR_Exporter(browser=args.browser, choose_profile=False)

        for url in sites:
            print(f"\n--- Visiting {url} ---")
            driver.get(url, wait_time=10)
            current = driver.driver.current_url
            print(f"  Landed on: {current}")

            try:
                # — Social media custom —
                if "youtube.com" in url or "youtube.com" in current:
                    # reload home & search “cats”
                    driver.get("https://www.youtube.com", wait_time=5)
                    search_box = driver.find_element(By.NAME, 'search_query')
                    search_box.clear()
                    search_box.send_keys("cats")
                    search_box.send_keys(Keys.RETURN)
                    time.sleep(3)

                    videos = driver.find_elements(By.XPATH, '//a[@id="video-title"]')
                    actual = next((v for v in videos
                                   if v.get_attribute('href') and "/watch?v=" in v.get_attribute('href')), None)
                    if actual:
                        href = actual.get_attribute('href')
                        print(f"   → YouTube: clicking {href}")
                        actual.click()
                        time.sleep(20)
                    else:
                        print("   ! YouTube: no videos found")

                elif "reddit.com" in url or "reddit.com" in current:
                     
                    driver.get("https://old.reddit.com", wait_time=10)
                    posts = driver.find_elements(By.CSS_SELECTOR, "div.thing a.title")
                    if posts:
                        href = posts[0].get_attribute("href")
                        print(f"   → Reddit: clicking {href}")
                        posts[0].click()
                        time.sleep(10)
                    else:
                        print("   ! Reddit: no post links found")
                elif "tumblr.com" in current:
                     print("  → [Tumblr branch]")

                   # load the Tumblr homepage
                     driver.get("https://www.tumblr.com", wait_time=10)

                    # scroll 
                     driver.execute_script("window.scrollBy(0, 1000);")
                     time.sleep(5)

                      #try real post links
                     posts = driver.find_elements(By.CSS_SELECTOR, "a[href*='/post/']")
                     if posts:
                        href = posts[0].get_attribute("href")
                        print(f"    clicking Tumblr post: {href}")
                        posts[0].click()
                        time.sleep(10)

                
                elif "stackoverflow.com" in url or "stackoverflow.com" in current:
                     print("  → [StackOverflow branch]")

                     # wait for question links to appear
                     wait = WebDriverWait(driver.driver, 15)
                     wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "a.question-hyperlink")))

                     posts = driver.find_elements(By.CSS_SELECTOR, "a.question-hyperlink")
                     if posts:
                        href = posts[0].get_attribute("href")
                        print(f"    clicking question link: {href}")
                     # scroll it into view so it's interactable
                        driver.driver.execute_script("arguments[0].scrollIntoView(true);", posts[0])
                        posts[0].click()
                        time.sleep(10)
                     else:
                         print("    ! StackOverflow: no question links found")


                if category == "News":
                   print("  → [News branch]")
                   wd = driver.driver
                  # figure out the loaded hostname (strip off any “www.”)
                   current_page = wd.current_url   
                   root = urlparse(current_page).netloc.replace("www.", "")
    
    
                   if root == "wikipedia.org":
                    # search for “JD Vance" :)
                      # wait for the search box to be clickable
                      WebDriverWait(wd, 10).until(
                          EC.element_to_be_clickable((By.ID, "searchInput"))
        )
                      search_box = wd.find_element(By.ID, "searchInput")
                      search_box.clear()
                      search_box.send_keys("JD Vance", Keys.RETURN)
                      WebDriverWait(wd, 10).until(
                          EC.presence_of_element_located(("css selector", "ul.mw-search-results li div a"))
        )
                      first = wd.find_element(By.CSS_SELECTOR, "ul.mw-search-results li div a")
                      href = first.get_attribute("href")
                      print(f"    → clicking first Wikipedia result: {href}")
                      wd.execute_script("arguments[0].scrollIntoView(true);", first)
                      first.click()
                      time.sleep(10)
                
                   elif root == "cnn.com":
                        print("  → [CNN branch]")
                        time.sleep(5)  
                        headlines = wd.find_elements(By.CSS_SELECTOR, "a.container__title-url")
                        if headlines:
                           href = headlines[0].get_attribute("href")
                           print(f"    → clicking CNN headline: {href}")
                           wd.execute_script("window.open('{}','_blank')".format(href))
                           time.sleep(5)
                        else:
                           print("    ! CNN: no headlines found")
                   elif root.endswith("vox.com"):
                         print("  → [Vox branch]")
                         time.sleep(5)  

                         cards = wd.find_elements(By.CSS_SELECTOR, "a.qcd9z1")
                         if cards:
                            # build the absolute URL
                            href = urljoin(current_page, cards[0].get_attribute("href"))
                            print(f"    → opening Vox story: {href}")

                            # (bypasses interactability)
                            wd.execute_script("window.open(arguments[0], '_blank');", href)

                            time.sleep(7)
                         else:
                           print("    ! Vox: no elements matching a.qcd9z1")

                   else:
              # GENERAL CASE: find first internal article link
                     article = None
                     for link in wd.find_elements(By.TAG_NAME, "a"):
                         href = link.get_attribute("href") or ""
                         parsed = urlparse(href)
            
            # relative URL → treat as internal
                         if not parsed.netloc and parsed.path not in ("", "/"):
                            real_href = urljoin(current_page, parsed.path)
                            article = link
                            break
            
            # absolute URL → compare stripped hostnames
                         host = parsed.netloc.replace("www.", "")
                         if parsed.scheme in ("http", "https") \
                           and host.endswith(root) \
                           and parsed.path not in ("", "/") \
                           and not parsed.fragment:
                             real_href = href
                             article = link
                             break
        
        # click or fall back
                         if article:
                             print(f"    → clicking first article on {root}: {real_href}")
                             wd.execute_script("arguments[0].scrollIntoView(true);", article)
                             article.click()
                             time.sleep(7)
                         #else:
                             #print(f"    ! News: no article found on {root}, falling back…")
        
                             wd.execute_script("window.scrollBy(0, window.innerHeight);")
                             time.sleep(3)

                             wd.execute_script("window.scrollBy(0, 1000);")
                             time.sleep(1)
                elif category == "Shopping":
                      print("  → [Shopping branch]")
                      wd = driver.driver
                      current_page = wd.current_url
                      root = urlparse(current_page).netloc.replace("www.", "")
                      term = "nike shoes"

                      if root.endswith("amazon.com"):
                          print("  → [Amazon branch]")
                          #wd = driver.driver
                          term = "nike shoes"
                          search_url = f"https://www.amazon.com/s?k={urllib.parse.quote(term)}"
                          driver.get(search_url, wait_time=10)
                          wd = driver.driver
                          if "Sorry, something went wrong" in wd.page_source:
                             print("    → hit error page, retrying search URL…")
                             driver.get(search_url, wait_time=10)
                             wd = driver.driver
                          '''
                          WebDriverWait(wd, 10).until(
                          EC.presence_of_element_located((By.ID, "twotabsearchtextbox"))
                           )
                          search = wd.find_element(By.ID, "twotabsearchtextbox")  # <input id="twotabsearchtextbox" …> :contentReference[oaicite:0]{index=0}
                          search.clear()
                          search.send_keys(term)
                          #time.sleep(5)
   
                          try:
                             wd.find_element(By.ID, "nav-search-submit-button").click()
                          except:
                             search.send_keys(Keys.RETURN)
                        '''
                             #time.sleep(5)
                          # wait for at least one real result-item to appear
                          product_link_sel = (
                                          "div[data-component-type='s-search-result'] "
                                          "a.a-link-normal.s-line-clamp-2.s-link-style.a-text-normal[href*='/dp/']"
)
                         # whose URL goes to /dp/



                          WebDriverWait(wd, 15).until(
                              EC.presence_of_element_located((By.CSS_SELECTOR, product_link_sel))
)
                          results = wd.find_elements(By.CSS_SELECTOR, product_link_sel)
                                #"div.s-main-slot div[data-component-type='s-search-result'] h2 a"
    
                          if results:
                             href = results[0].get_attribute("href")
                             print(f"    → clicking first Amazon result: {href}")
                             wd.get(href)
                             
                             WebDriverWait(wd, 15).until( 
                                 EC.presence_of_element_located((By.ID, "productTitle"))
                             
)
                             wd.execute_script("window.scrollBy(0, window.innerHeight);")
                             
                          else:
                              print("    ! Amazon: no search results found")

                      elif root.endswith("ebay.com"):
                           print("  → [eBay branch]")
                           wd = driver.driver
                           #original_url = wd.current_url  # Store original URL
                           term = "dior"

                           
                           print("    Waiting for search box...")
                           WebDriverWait(wd, 15).until(EC.presence_of_element_located((By.ID, "gh-ac")))
                           search = wd.find_element(By.ID, "gh-ac")
                           search.clear()
                           search.send_keys(term, Keys.RETURN)
                           print("    Search submitted...")

                           print("    Waiting for results...")
                           WebDriverWait(wd, 15).until(EC.presence_of_element_located((
                           By.CSS_SELECTOR,"a.s-item__link" 
        )))                    
                           print("    Scrolling search results...")
                           wd.execute_script("window.scrollBy(0, window.innerHeight / 2);")
                           time.sleep(2)
                           continue
        
                                
                           

                else:
                    links = driver.find_elements(By.TAG_NAME, "a")
                    for link in links:
                        href = link.get_attribute("href") or ""
                        if href.startswith("http"):
                            print(f"   → Generic: clicking {href}")
                            link.click()
                            time.sleep(10)
                            break

                print(f"  → After click: {driver.driver.current_url}")
             
            except Exception as e:
                print(f"  ! Error on {url}: {e}")

        # Export HAR for each domain in domains.tx
        har_path = driver.export_har()
        print(f"HAR for {category} written to {har_path}")

        driver.quit()

    




