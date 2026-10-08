document.querySelector('#state').textContent = '当前场景：' + (new URLSearchParams(location.search).get('state') || 'entry')
document.querySelector('#action').addEventListener('click', () => { document.querySelector('#result').textContent = '相对脚本已执行' })
