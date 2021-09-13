import cinemaFacts

def test_main(capsys):

   out, err = capsys.readouterr()
   assert out == 'Success'
   assert err == ''
