class TrafficInfo():
    def __init__(self, client):
        self.traffic_info = client.monitoring.traffic_statistics()

    # in bps
    def get_download_rate(self):
        return int(self.traffic_info['CurrentDownloadRate']) * 8

    # in bps
    def get_upload_rate(self):
        return int(self.traffic_info['CurrentUploadRate']) * 8
