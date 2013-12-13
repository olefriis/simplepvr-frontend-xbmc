directory 'output'

desc 'Package XBMC plug-in'
task :package => 'output' do
  zip_file_name = 'output/plugin.video.simplepvr-0.0.3.zip'
  File.delete zip_file_name if File.exists? zip_file_name
  `find . -name '*.pyc' -delete`
  `find . -name '__pycache__' -delete`
  `zip -r #{zip_file_name} plugin.video.simplepvr`
end

task :default => ['package']