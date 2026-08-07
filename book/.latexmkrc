$ENV{'TEXINPUTS'} = './lib//:' . ($ENV{'TEXINPUTS'} // '');
$pdf_mode = 1;
$bibtex_use = 2;
$pdflatex = 'pdflatex -interaction=nonstopmode -file-line-error %O %S';
$clean_ext = 'synctex.gz';

add_cus_dep('glo', 'gls', 0, 'makeglossaries');
add_cus_dep('glo', 'glg', 0, 'makeglossaries');

sub makeglossaries {
  my ($base) = @_;
  system("makeglossaries", $base);
}
