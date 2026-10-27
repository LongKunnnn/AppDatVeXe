package com.vexeapp.utils;

import java.text.Normalizer;
import java.util.HashMap;
import java.util.Map;
import java.util.regex.Pattern;

public class OSMRouteLibrary {

    public static class RouteInfo {
        public String distance;
        public String time;

        public RouteInfo(String distance, String time) {
            this.distance = distance;
            this.time = time;
        }
    }

    private static final Map<String, RouteInfo> routeData = new HashMap<>();

    static {
        // Tọa độ thực tế từ OSM
        // Hà Nội: 21.0285, 105.8542
        // Ninh Bình: 20.2506, 105.9745
        // Thanh Hóa: 19.8067, 105.7852

        // Cài đặt dữ liệu lộ trình thực tế (Road Distance) từ OSM
        addRoute("Hà Nội", "Ninh Bình", "95 km", "1 giờ 30 phút");
        addRoute("Ninh Bình", "Hà Nội", "95 km", "1 giờ 30 phút");
        
        addRoute("Hà Nội", "Thanh Hóa", "160 km", "2 giờ 30 phút");
        addRoute("Thanh Hóa", "Hà Nội", "160 km", "2 giờ 30 phút");
        
        addRoute("Ninh Bình", "Thanh Hóa", "65 km", "1 giờ 15 phút");
        addRoute("Thanh Hóa", "Ninh Bình", "65 km", "1 giờ 15 phút");
    }

    private static void addRoute(String start, String end, String dist, String time) {
        String key = normalize(start) + "_" + normalize(end);
        routeData.put(key, new RouteInfo(dist, time));
    }

    public static RouteInfo getRoute(String start, String end) {
        if (start == null || end == null) return null;
        String key = normalize(start) + "_" + normalize(end);
        return routeData.get(key);
    }

    // Hàm chuẩn hóa tiếng Việt: bỏ dấu, viết thường để tìm kiếm thông minh
    public static String normalize(String str) {
        if (str == null) return "";
        String nfdNormalizedString = Normalizer.normalize(str, Normalizer.Form.NFD);
        Pattern pattern = Pattern.compile("\\p{InCombiningDiacriticalMarks}+");
        return pattern.matcher(nfdNormalizedString).replaceAll("")
                .toLowerCase()
                .replace("đ", "d")
                .trim();
    }
}
