
#authentication
def check(user, pw):
	if pw == "admin" and user == "admin":
		return True
	else:
		return False

