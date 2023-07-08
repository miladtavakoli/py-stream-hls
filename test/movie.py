import io
from unittest import mock

from test import BaseStreamTestCase, app
from repository.user import User

from use_case.movie import CreateMovie
from werkzeug.datastructures import FileStorage


class CreateMovieUseCaseTestCase(BaseStreamTestCase):

    def setUp(self):
        super(CreateMovieUseCaseTestCase, self).setUp()
        self.valid_movie_data = {
            "title": "This test Title",
            "description": "This test description... !",
            "imdb_tag": "ttNevermind",
            "movie_file": FileStorage(stream=io.BytesIO(b"MP4 Is heree:)))"),
                                      filename='test.mp4',
                                      content_type="video/mpeg",
                                      ),
            "thumbnail_file": FileStorage(io.BytesIO(b"Jpeg Is heree:)))"),
                                          filename='test.jpg',
                                          content_type='image/jpeg'
                                          ),
        }

    @mock.patch('celery_tasks.tasks.task_create_hls_files.delay')
    @mock.patch('ffmpeg.create_hls_files')
    @mock.patch.object(CreateMovie, '_save_movie')
    @mock.patch.object(CreateMovie, '_save_movie_thumbnail')
    def test_create_movie_use_case(self, mock_save_thumbnail, mock_save_movie, mock_create_hls_files, mock_celery_task):
        mock_save_thumbnail.return_value = "test.jpg"
        mock_save_movie.return_value = "test.mp4"
        mock_create_hls_files.return_value = "noob_stream.m3u8"
        mock_celery_task.return_value = True
        with app.app_context():
            user = User()
            user.username = 'admin'
            user.password = 'admin'
            user.email = 'info@noobot.ir'
            user.save()
            has_error, result = CreateMovie(input_data=self.valid_movie_data, user_id=user.id).run()
            self.assertFalse(has_error)
            self.assertIn('msg', result)
            self.assertIn('data', result)
            self.assertEqual('Upload movie successful...', result['msg'])
            self.assertEqual(self.valid_movie_data['title'], result['data'].title)
            self.assertEqual(self.valid_movie_data['description'], result['data'].description)
            self.assertEqual(self.valid_movie_data['imdb_tag'], result['data'].imdb_tag)
            self.assertEqual("test.mp4", result['data'].original_filename)
            self.assertEqual("test.jpg", result['data'].thumbnail)
