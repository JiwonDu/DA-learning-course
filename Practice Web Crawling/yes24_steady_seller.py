import requests
from bs4 import BeautifulSoup
import csv
import pymysql
from datetime import datetime

class Book:
    def __init__(self, rank, title, author, publisher, pub_date, price):
        self.rank = rank
        self.title = title
        self.author = author
        self.publisher = publisher
        self.pub_date = pub_date
        self.price = price
    
    def __str__(self):
        return f"{self.rank}위: {self.title} / 저자: {self.author} / 출판사: {self.publisher} / 출간일: {self.pub_date} / 가격: {self.price}"

    def to_dict(self):
        return {
            'rank': self.rank,
            'title': self.title,
            'author': self.author,
            'publisher': self.publisher,
            'pub_date': self.pub_date,
            'price': self.price
        }
    
    def to_list(self):
        return [self.rank, self.title, self.author, self.publisher, self.pub_date, self.price]

url = 'https://www.yes24.com/Product/Category/SteadySeller?categoryNumber=001'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

book_list_element = soup.select("#yesBestList > li")
book_list = []

for i, item in enumerate(book_list_element, 1):
    try:
        book_title = item.select_one('div.item_info > div.info_row.info_name > a.gd_name').text.strip()
        book_author = item.select_one('div.item_info > div.info_row.info_pubGrp > span.authPub.info_auth > a').text.strip()
        book_publisher = item.select_one('div.item_info > div.info_row.info_pubGrp > span.authPub.info_pub > a').text.strip()
        book_pub_date = item.select_one('div.item_info > div.info_row.info_pubGrp > span.authPub.info_date').text.strip()
        book_price = item.select_one('div.item_info > div.info_row.info_price > strong > em').text.strip()
        
        book_list.append(Book(i, book_title, book_author, book_publisher, book_pub_date, book_price))
    except AttributeError as e:
        print(f"{i}번째 도서 처리 중 오류: {e}")
        continue

print("\n=== 크롤링된 도서 목록 ===")
for book in book_list:
    print(book)

# CSV 파일로 저장
csv_filename = f'steady_books_{datetime.now().strftime("%Y%m%d")}.csv'
with open(csv_filename, 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['순위', '제목', '저자', '출판사', '출간일', '가격'])
    for book in book_list:
        writer.writerow(book.to_list())

print(f'\nCSV 파일 저장 완료: {csv_filename}')

# MySQL DB 연결 및 데이터 저장
config = {
    'host': 'localhost',
    'user': 'root',
    'password': '1234',
    'database': 'yes24_steady',
    'charset': 'utf8mb4'
}

try:
    print("\nMySQL 연결 중...")
    conn = pymysql.connect(**config)
    cur = conn.cursor()
    print("MySQL 연결 성공")
    
    print("기존 데이터 삭제 중...")
    cur.execute('DELETE FROM books')
    
    print("새로운 데이터 삽입 중...")
    inserted_count = 0
    
    for book in book_list:
        data = book.to_list()
        try:
            cur.execute('''
                INSERT INTO books (book_rank, title, author, publisher, pub_date, price)
                VALUES (%s, %s, %s, %s, %s, %s)
            ''', data)
            inserted_count += 1
            print(f"삽입 성공: {book.title}")
        except Exception as e:
            print(f"삽입 실패: {book.title}")
            print(f"오류 내용: {e}")
            continue

    conn.commit()
    print(f'\n총 {inserted_count}개의 데이터 삽입 완료')

    print("\n=== MySQL DB 저장된 데이터 확인 ===")
    cur.execute('SELECT COUNT(*) FROM books')
    count = cur.fetchone()[0]
    print(f"저장된 총 데이터 수: {count}")

    if count > 0:
        print("\n처음 5개 데이터:")
        cur.execute('SELECT * FROM books LIMIT 5')
        rows = cur.fetchall()
        for row in rows:
            print(row)

except Exception as e:
    print(f"\nMySQL 오류:")
    print(f"오류 유형: {type(e).__name__}")
    print(f"오류 내용: {str(e)}")
    if hasattr(e, 'errno'):
        print(f"오류 번호: {e.errno}")

finally:
    if 'cur' in locals():
        cur.close()
    if 'conn' in locals():
        conn.close()
    print("\nMySQL 연결 종료")
