interface Measurement {
    id: number;
    operator: {
      id: number;
      name: string;
    };
    voice_service_non_accessibility: number;
    voice_service_cut_off: number;
    speech_quality_on_call: number;
    negative_mos_samples_ratio: number;
    undelivered_messages: number;
    avg_sms_delivery_time: number;
    http_failure_session: number;
    http_ul_mean_userdata_rate: number;
    http_dl_mean_userdata_rate: number;
    http_session_time: number;
    number_of_test_voice_connections: number;
    number_of_voice_sequences: number;
    voice_connections_with_low_intelligibility: number;
    number_of_sms_messages: number;
    number_of_connections_attempts_http: number;
    number_of_test_sessions_http: number;
  }
  
  export interface MeasurementKeys extends Omit<Measurement, "id"> {}
  
  export interface Report {
    region: string;
    place: string;
    from: string;
    to: string;
    measurements: Measurement[];
  }

  export interface IReportUpload {
    files: FileList;
  }