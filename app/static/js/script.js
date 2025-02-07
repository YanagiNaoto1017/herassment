
       document.getElementById('harassmentForm').onsubmit = async (event) => {
           event.preventDefault();
           const content = document.getElementById('content').value;
           const response = await fetch('/analyze-content/', {
               method: 'POST',
               headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
               body: `content=${encodeURIComponent(content)}`
           });
           const data = await response.json();
           document.getElementById('result').innerText = data.is_harassment
               ? "ハラスメントが検出されました。"
               : "ハラスメントは検出されませんでした。";
       };

       function toggleMenu() {
        var sidebar = document.getElementById('sidebar');
        var overlay = document.getElementById('overlay');
        sidebar.classList.toggle('active');
        overlay.classList.toggle('active');
    }