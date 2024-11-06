// 다크모드 토글
const darkModeToggle = document.getElementById('darkModeToggle');
const body = document.body;

darkModeToggle.addEventListener('click', () => {
    body.classList.toggle('dark-mode');
    localStorage.setItem('darkMode', body.classList.contains('dark-mode'));
});

// 다크모드 상태 유지
if (localStorage.getItem('darkMode') === 'true') {
    body.classList.add('dark-mode');
}

// 푸터 타이핑 애니메이션
const text = "Success is the sum of small efforts, repeated day in and day out. - Robert Collier";
const typingText = document.getElementById('typing-text');
let i = 0;

function typeWriter() {
    if (i < text.length) {
        typingText.innerHTML += text.charAt(i);
        i++;
        setTimeout(typeWriter, 50);
    }
}

typeWriter();

// 스크롤 진행 표시기
window.onscroll = function() {scrollProgress()};

function scrollProgress() {
    let winScroll = document.body.scrollTop || document.documentElement.scrollTop;
    let height = document.documentElement.scrollHeight - document.documentElement.clientHeight;
    let scrolled = (winScroll / height) * 100;
    
    if (!document.getElementById("progressBar")) {
        let progressBar = document.createElement("div");
        progressBar.id = "progressBar";
        progressBar.style.position = "fixed";
        progressBar.style.top = "0";
        progressBar.style.left = "0";
        progressBar.style.height = "5px";
        progressBar.style.backgroundColor = "#4CAF50";
        progressBar.style.zIndex = "9999";
        document.body.appendChild(progressBar);
    }
    
    document.getElementById("progressBar").style.width = scrolled + "%";
}