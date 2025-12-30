"""
인스타그램 데이터 수집 스크립트
Selenium을 활용하여 인스타그램 계정의 게시물 데이터를 수집합니다.
참고: https://hamhands.tistory.com/entry/챗gpt로-인스타그램-크롤링-하기인스타-api-없이-크롤링-성공
"""

import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import json
import os
from datetime import datetime
import logging

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/instagram_crawler.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class InstagramCrawler:
    """인스타그램 크롤러 클래스"""
    
    def __init__(self, headless=False, wait_time=10):
        """
        초기화
        
        Parameters:
        -----------
        headless : bool
            브라우저를 백그라운드에서 실행할지 여부
        wait_time : int
            요소를 찾기 위한 대기 시간 (초)
        """
        self.wait_time = wait_time
        self.driver = None
        self.setup_driver(headless)
        self.posts_data = []
    
    def setup_driver(self, headless=False):
        """Chrome 드라이버 설정"""
        chrome_options = Options()
        if headless:
            chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        chrome_options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
        
        try:
            self.driver = webdriver.Chrome(options=chrome_options)
            self.driver.implicitly_wait(self.wait_time)
            logger.info("Chrome 드라이버 초기화 완료")
        except Exception as e:
            logger.error(f"드라이버 초기화 실패: {str(e)}")
            raise
    
    def login(self, username, password):
        """
        인스타그램 로그인
        
        Parameters:
        -----------
        username : str
            인스타그램 사용자명
        password : str
            비밀번호
        """
        try:
            logger.info("인스타그램 로그인 페이지 접속 중...")
            self.driver.get("https://www.instagram.com/accounts/login/")
            time.sleep(3)
            
            # 사용자명 입력
            username_input = WebDriverWait(self.driver, self.wait_time).until(
                EC.presence_of_element_located((By.NAME, "username"))
            )
            username_input.send_keys(username)
            
            # 비밀번호 입력
            password_input = self.driver.find_element(By.NAME, "password")
            password_input.send_keys(password)
            password_input.send_keys(Keys.RETURN)
            
            time.sleep(5)
            
            # 로그인 성공 확인
            if "instagram.com" in self.driver.current_url and "login" not in self.driver.current_url:
                logger.info("로그인 성공")
                return True
            else:
                logger.warning("로그인 실패 가능성 - 수동으로 확인 필요")
                return False
                
        except Exception as e:
            logger.error(f"로그인 중 오류 발생: {str(e)}")
            return False
    
    def get_account_posts(self, account_name, num_posts=20, scroll_pause_time=2):
        """
        특정 계정의 게시물 데이터 수집
        
        Parameters:
        -----------
        account_name : str
            인스타그램 계정명 (예: 'canu_official')
        num_posts : int
            수집할 게시물 개수
        scroll_pause_time : int
            스크롤 후 대기 시간 (초)
        
        Returns:
        --------
        list
            게시물 데이터 리스트
        """
        try:
            logger.info(f"{account_name} 계정 페이지 접속 중...")
            self.driver.get(f"https://www.instagram.com/{account_name}/")
            time.sleep(3)
            
            # 첫 번째 게시물 클릭
            try:
                first_post = WebDriverWait(self.driver, self.wait_time).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "article a"))
                )
                first_post.click()
                time.sleep(2)
            except TimeoutException:
                logger.warning("게시물을 찾을 수 없습니다.")
                return []
            
            collected_posts = 0
            self.posts_data = []
            
            while collected_posts < num_posts:
                try:
                    post_data = self._extract_post_data(account_name)
                    if post_data:
                        self.posts_data.append(post_data)
                        collected_posts += 1
                        logger.info(f"{collected_posts}/{num_posts} 게시물 수집 완료")
                    
                    # 다음 게시물로 이동
                    if collected_posts < num_posts:
                        next_button = self.driver.find_element(
                            By.CSS_SELECTOR, 
                            "button[aria-label='다음']"  # 또는 "button._abl-"
                        )
                        if next_button.is_enabled():
                            next_button.click()
                            time.sleep(scroll_pause_time)
                        else:
                            logger.info("더 이상 게시물이 없습니다.")
                            break
                            
                except NoSuchElementException:
                    logger.warning("다음 게시물 버튼을 찾을 수 없습니다.")
                    break
                except Exception as e:
                    logger.error(f"게시물 수집 중 오류: {str(e)}")
                    break
            
            logger.info(f"총 {len(self.posts_data)}개 게시물 수집 완료")
            return self.posts_data
            
        except Exception as e:
            logger.error(f"게시물 수집 중 오류 발생: {str(e)}")
            return []
    
    def _extract_post_data(self, account_name):
        """
        현재 페이지의 게시물 데이터 추출
        
        Parameters:
        -----------
        account_name : str
            계정명
        
        Returns:
        --------
        dict
            게시물 데이터
        """
        try:
            post_data = {
                'account': account_name,
                'post_url': self.driver.current_url,
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            
            # 게시물 본문 추출
            try:
                # 여러 가능한 선택자 시도
                caption_selectors = [
                    "article h1",
                    "article span",
                    "div[role='dialog'] span",
                    "h1._aacl"
                ]
                
                caption = ""
                for selector in caption_selectors:
                    try:
                        caption_element = self.driver.find_element(By.CSS_SELECTOR, selector)
                        caption = caption_element.text
                        if caption:
                            break
                    except:
                        continue
                
                post_data['caption'] = caption
            except:
                post_data['caption'] = ""
            
            # 좋아요 수 추출
            try:
                like_selectors = [
                    "section button span",
                    "a[href*='/liked_by/'] span",
                    "span._ac2a"
                ]
                
                likes = ""
                for selector in like_selectors:
                    try:
                        like_elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                        for elem in like_elements:
                            text = elem.text.strip()
                            if '좋아요' in text or 'like' in text.lower() or text.replace(',', '').replace('.', '').isdigit():
                                likes = text
                                break
                        if likes:
                            break
                    except:
                        continue
                
                post_data['likes'] = likes
            except:
                post_data['likes'] = "N/A"
            
            # 댓글 수 추출
            try:
                comment_selectors = [
                    "a[href*='/comments/'] span",
                    "span._ac2a",
                    "ul span"
                ]
                
                comments = ""
                for selector in comment_selectors:
                    try:
                        comment_elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                        for elem in comment_elements:
                            text = elem.text.strip()
                            if '댓글' in text or 'comment' in text.lower():
                                comments = text
                                break
                        if comments:
                            break
                    except:
                        continue
                
                post_data['comments'] = comments
            except:
                post_data['comments'] = "N/A"
            
            return post_data
            
        except Exception as e:
            logger.error(f"게시물 데이터 추출 중 오류: {str(e)}")
            return None
    
    def save_to_csv(self, filename='data/instagram_posts.csv'):
        """
        수집한 데이터를 CSV 파일로 저장
        
        Parameters:
        -----------
        filename : str
            저장할 파일 경로
        """
        if not self.posts_data:
            logger.warning("저장할 데이터가 없습니다.")
            return
        
        os.makedirs(os.path.dirname(filename) if os.path.dirname(filename) else '.', exist_ok=True)
        
        df = pd.DataFrame(self.posts_data)
        df.to_csv(filename, index=False, encoding='utf-8-sig')
        logger.info(f"데이터 저장 완료: {filename}")
        return df
    
    def save_to_json(self, filename='data/instagram_posts.json'):
        """
        수집한 데이터를 JSON 파일로 저장
        
        Parameters:
        -----------
        filename : str
            저장할 파일 경로
        """
        if not self.posts_data:
            logger.warning("저장할 데이터가 없습니다.")
            return
        
        os.makedirs(os.path.dirname(filename) if os.path.dirname(filename) else '.', exist_ok=True)
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.posts_data, f, ensure_ascii=False, indent=2)
        logger.info(f"데이터 저장 완료: {filename}")
    
    def close(self):
        """브라우저 종료"""
        if self.driver:
            self.driver.quit()
            logger.info("브라우저 종료 완료")


def main():
    """메인 실행 함수"""
    # 사용자 설정
    INSTAGRAM_USERNAME = "your_username"  # 실제 사용자명으로 변경
    INSTAGRAM_PASSWORD = "your_password"  # 실제 비밀번호로 변경
    ACCOUNT_TO_CRAWL = "canu_official"    # 크롤링할 계정명
    NUM_POSTS = 20                        # 수집할 게시물 개수
    
    crawler = None
    
    try:
        # 디렉토리 생성
        os.makedirs('data', exist_ok=True)
        os.makedirs('logs', exist_ok=True)
        
        # 크롤러 초기화
        crawler = InstagramCrawler(headless=False)  # headless=True로 설정하면 브라우저 창이 안 보임
        
        # 로그인 (선택사항 - 공개 계정은 로그인 없이도 가능)
        # crawler.login(INSTAGRAM_USERNAME, INSTAGRAM_PASSWORD)
        
        # 게시물 수집
        posts = crawler.get_account_posts(ACCOUNT_TO_CRAWL, num_posts=NUM_POSTS)
        
        if posts:
            # 데이터 저장
            df = crawler.save_to_csv('data/instagram_posts.csv')
            crawler.save_to_json('data/instagram_posts.json')
            
            # 결과 출력
            print("\n" + "="*60)
            print("수집 결과 요약")
            print("="*60)
            print(f"수집된 게시물 수: {len(posts)}개")
            print(f"\n데이터 미리보기:")
            print(df.head())
            print("\n데이터가 'data/instagram_posts.csv'에 저장되었습니다.")
        else:
            print("게시물을 수집하지 못했습니다.")
        
    except KeyboardInterrupt:
        logger.info("사용자에 의해 중단되었습니다.")
    except Exception as e:
        logger.error(f"오류 발생: {str(e)}")
    finally:
        if crawler:
            crawler.close()


if __name__ == '__main__':
    main()

