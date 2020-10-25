package com.sample.mask;

import android.app.Activity;
import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.widget.Toast;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;

import com.naver.maps.geometry.LatLng;
import com.naver.maps.map.MapView;
import com.naver.maps.map.NaverMap;
import com.naver.maps.map.OnMapReadyCallback;
import com.naver.maps.map.overlay.Marker;
import com.naver.maps.map.overlay.Overlay;
import android.view.View;

public class MapsNaverActivity extends Activity implements OnMapReadyCallback {

    private MapView mapView;

    @Override
    protected void onCreate(@Nullable Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_maps_naver);

        mapView = findViewById(R.id.map_view);

        mapView.getMapAsync(this);

    }

    @Override
    public void onMapReady(@NonNull NaverMap naverMap) {
        Marker marker = new Marker();
        marker.setPosition(new LatLng(37.5670135, 126.9783740));
        marker.setMap(naverMap);
        marker.setOnClickListener(new Overlay.OnClickListener() {
            @Override
            public boolean onClick(@NonNull Overlay overlay) {
                Intent intent = new Intent(getApplicationContext(),MainActivity.class);
                startActivity(intent);
                return false;
            }
        });
    }

}
