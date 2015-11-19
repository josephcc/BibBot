
require 'json'

require 'sinatra'
PUBLIC_FOLDER = File.join File.dirname(__FILE__), 'dist'
set :public_folder, PUBLIC_FOLDER
set :bind, '128.2.178.35'
set :port, '9999'
set :environment, :production
set :server, :puma

require './model.rb'

Encoding.default_external = Encoding::UTF_8

get '/' do
  send_file File.join(PUBLIC_FOLDER, 'index.html')
end

get '/api/list' do
  content_type :json
  {:data => Citation.last(100)}.to_json
end

