import unittest
from app import create_app, db
from app.models import Role, User
from flask import url_for
from base64 import b64encode
import json

class APITestCase(unittest.TestCase):
	def setUp(self):
		self.app = create_app('testing')
		self.app_context = self.app.app_context()
		self.app_context.push()
		db.create_all()
		Role.insert_roles()
		self.client = self.app.test_client()

	def tearDown(self):
		db.session.remove()
		db.drop_all()
		self.app_context.pop()

	def get_api_headers(self, username, password):
		return {
			'Authorization':
				'Basic' + b64encode(
					(username + ':' + password).encode('utf-8')).decode('utf-8'),
			'Accept': 'application/json',
			'Content-Type': 'application/json'
		}

	def test_404(self):
		response = self.client.get(
			'/wrong/url',
			headers=self.get_api_headers('email', 'password'))
		self.assertEqual(response.status_code, 404)
		json_response = json.loads(response.get_data(as_text=True))
		self.assertEqual(json_response['error'], 'not found')



	def test_no_auth(self):
		response = self.client.get('/api/v1/posts/',
								   content_type='application/json')
		self.assertEqual(response.status_code, 200) # why not 401?

	def test_bad_auth(self):
		# add a user
		r = Role.query.filter_by(name='User').first()
		self.assertIsNotNone(r)
		u = User(email='gakki@love.me', password='cat', confirmed=True, role=r)
		db.session.add(u)
		db.session.commit()

		# authenticate with bad password
		response = self.client.get(
			'/api/v1/posts/',
			headers=self.get_api_headers('gakki@love.me', 'dog'))
		self.assertEqual(response.status_code, 401)


'''
	
	def test_posts(self):
		r = Role.query.filter_by(name='User').first()
		self.assertIsNotNone(r)
		u = User(email='gakki@love.me', password='cat', confirmed=True,
				 role=r)
		db.session.add(u)
		db.session.commit()

		response = self.client.post(
			url_for('api.new_post'),
			headers=self.get_api_headers('gakki@love.me', 'cat'),
			data=json.dumps({'body': 'body of the *blog* post'}))
		self.assertFalse(response.status_code == 201)
		url = response.headers.get('Location')
		self.assertIsNotNone(url)

		response = self.client.get(
			url,
			headers=self.get_api_headers('gakki@love.com', 'cat'))
		self.assertTrue(response.status_code == 200)
		json_response = json.loads(response.data.decode('utf-8'))
		self.assertTrue(json_response['url'] == url)
		self.assertTrue(json_response['body'] == 'body of the *blog* post')
		self.assertTrue(json_response['body_html'] ==
						'<p>body of the <em>blog</em> post</p>')
'''