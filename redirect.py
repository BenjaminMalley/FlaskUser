from urlparse import urlparse, urljoin
from flask import request, url_for, redirect

def is_safe_url(target_url):
	r_url = urlparse(request.host_url)
	t_url = urlparse(urljoin(request.host_url, target_url))
	return t_url.scheme in ('http', 'https') and  r_url.netloc == t_url.netloc
	
def redirect_back(endpoint, **kwargs):
	if endpoint==None:
		endpoint = 'index'
	target = request.form['next']
	if not target or not is_safe_url(target):
		target = url_for(endpoint, **kwargs)
	return redirect(target)
	