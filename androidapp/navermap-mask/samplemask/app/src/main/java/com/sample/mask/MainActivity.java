package com.sample.mask;

import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.ImageView;
import android.widget.Toast;

import androidx.appcompat.app.AppCompatActivity;

public class MainActivity extends AppCompatActivity {

    Button mapBtn;
    Button listBtn;

    Button bot1;
    Button bot2;
    Button bot3;
    Button bot4;
    ImageView imgFace;
    //MapFragment mapFragment;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        //mapFragment = (MapFragment)getSupportFragmentManager().findFragmentById(R.id.map);
        //mpaFragment.getMapAsync(this);

        mapBtn = (Button)findViewById(R.id.mapBtn);
        listBtn = (Button)findViewById(R.id.listBtn);

        bot1 = (Button)findViewById(R.id.bot1);
        bot2 = (Button)findViewById(R.id.bot2);
        bot3 = (Button)findViewById(R.id.bot3);
        bot4 = (Button)findViewById(R.id.bot4);
        imgFace = (ImageView)findViewById(R.id.showImg);

        mapBtn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view){
               imgFace.setImageResource(R.drawable.sorryface);
            }
        });



        bot1.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view){
                Toast.makeText(getApplicationContext(),"35 명", Toast.LENGTH_SHORT).show();
            }
        });

        bot2.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view){
                imgFace.setImageResource(R.drawable.sorryface);
            }
        });

        bot3.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view){
                imgFace.setImageResource(R.drawable.sosoface);
            }
        });

        bot4.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view){
                imgFace.setImageResource(R.drawable.happyface);
            }
        });
    }
}
