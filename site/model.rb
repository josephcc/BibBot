require 'sequel'

Sequel::Model.plugin :json_serializer
DB = Sequel.connect('postgres://josephcc:josephcc@localhost/bibbot', :max_connections => 8, :pool_timeout => 30)

class Citation < Sequel::Model(:bibbot)
end

