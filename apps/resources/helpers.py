class Helper:
    def responseRequest(self, status, msg, data, success):
        return {'success': success, 'message': msg,'data': data, 'status' : status }