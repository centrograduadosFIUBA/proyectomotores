fname = '20191209_151320.json';
val = jsondecode(fileread(fname));

samples = 31999;
samplesPorMedicion = 16;
timeStepNanos = 62500;

tNanos = 0:timeStepNanos:timeStepNanos*(samples);
tNanos = tNanos';
figure('Name','Diagnósticos Inteligentes: Dominio Temporal','NumberTitle','off');
figure(1);
subplot(3,1,1);
plot(tNanos,val.data_0,'r');
hold on;
plot(tNanos,val.data_4,'b');
hold off;
title('Phase 1');
legend('Current','Voltage');

subplot(3,1,2);
plot(tNanos,val.data_1,'r');
hold on;
plot(tNanos,val.data_5,'b');
hold off;
title('Phase 2');
legend('Current','Voltage');

subplot(3,1,3);
plot(tNanos,val.data_2,'r');
hold on;
plot(tNanos,val.data_6,'b');
hold off;
title('Phase 3');
legend('Current','Voltage');


figure('Name','Diagnósticos Inteligentes: Dominio Frecuencial','NumberTitle','off');
figure(2);
        
T = timeStepNanos / (10^9); %1/Fs;             % Sampling period 
Fs = 1/T; %1000;            % Sampling frequency   
L = length(val.data_0); %1500;             % Length of signal
t = (0:L-1)*T;        % Time vector

f = Fs*(0:(L/2))/L;

%%
subplot(3,1,1);

Y = fft(val.data_0); % DIRECTAMENTE GRAFICA:  pwelch(val.data_0,[],[],[],Fs);
P2 = abs(Y/L);
P1 = P2(1:L/2+1);
P1(2:end-1) = 2*P1(2:end-1);

plot(f(1:3300),P1(1:3300),'r') 
hold on;

Y = fft(val.data_4);
P2 = abs(Y/L);
P1 = P2(1:L/2+1);
P1(2:end-1) = 2*P1(2:end-1);

plot(f(1:3300),P1(1:3300),'b') 
hold off;
title('Phase 1 Spectrum');
legend('Current','Voltage');
xlabel('f (Hz)')
ylabel('|P1(f)|')

%%
subplot(3,1,2);

Y = fft(val.data_1);
P2 = abs(Y/L);
P1 = P2(1:L/2+1);
P1(2:end-1) = 2*P1(2:end-1);

plot(f(1:3300),P1(1:3300),'r') 
hold on;

Y = fft(val.data_5);
P2 = abs(Y/L);
P1 = P2(1:L/2+1);
P1(2:end-1) = 2*P1(2:end-1);

plot(f(1:3300),P1(1:3300),'b') 
hold off;
title('Phase 2 Spectrum');
legend('Current','Voltage');
xlabel('f (Hz)')
ylabel('|P1(f)|')

%%
subplot(3,1,3);

Y = fft(val.data_2);
P2 = abs(Y/L);
P1 = P2(1:L/2+1);
P1(2:end-1) = 2*P1(2:end-1);

plot(f(1:3300),P1(1:3300),'r') 
hold on;

Y = fft(val.data_6);
P2 = abs(Y/L);
P1 = P2(1:L/2+1);
P1(2:end-1) = 2*P1(2:end-1);

plot(f(1:3300),P1(1:3300),'b') 
hold off;
title('Phase 3 Spectrum');
legend('Current','Voltage');
xlabel('f (Hz)')
ylabel('|P1(f)|')

%%
% DIRECTAMENTE GRAFICA:  pwelch(val.data_0,[],[],[],Fs);% plomb es para
% cuando tengo señales con muestras perdidas.
%spectrogram

% incrementando el tamaño de ventana se mejora la resolucion de la fft (picos mas angostos)
% con ventanas chicas los picos se ven gordetes redondeados con poca resolucion, pudiendo ver
% un solo pico gordo enmascarando 2 o mas picos adentro que no se ven por falta de resolucion
% 
% 
% apenas tenga en on flags seteados cuando abs I >= 1000
% arranca primer segmento.

Ip1 = val.data_0(1046:end);
Ip2 = val.data_1(1046:end);
Ip3 = val.data_2(1046:end);


figure('Name','Diagnósticos Inteligentes: pwelch Corriente','NumberTitle','off');
figure(3);
subplot(3,1,1); pwelch(Ip1,[],[],[],Fs);
subplot(3,1,2); pwelch(Ip2,[],[],[],Fs);
subplot(3,1,3); pwelch(Ip3,[],[],[],Fs);

Nx = length(Ip1);
nsc = 1600; % (timeStepNanos/(10^9))*1600 = 100 ms
nov = floor(nsc/2); % overlap 50% (la mitad)
nff = max(256,2^nextpow2(nsc));

figure('Name','Diagnósticos Inteligentes: Espectrograma Ip1 con Hamming','NumberTitle','off');
figure(4);

spectrogram(Ip1,hamming(nsc),nov,nff,Fs,'yaxis','onesided');
caxis([-20 20]);

figure('Name','Diagnósticos Inteligentes: Espectrograma Ip2 con Hamming','NumberTitle','off');
figure(5);

spectrogram(Ip2,hamming(nsc),nov,nff,Fs,'yaxis','onesided');
caxis([-20 20]);

figure('Name','Diagnósticos Inteligentes: Espectrograma Ip3 con Hamming','NumberTitle','off');
figure(6);

spectrogram(Ip3,hamming(nsc),nov,nff,Fs,'yaxis','onesided');
caxis([-20 20]);

% [S,F,T,P] = spectrogram(Ip3,hamming(nsc),nov,nff,Fs,'yaxis','onesided');
% surf(T,F,10*log10(P),'edgecolor','none'); axis tight; view(0,90);
% set(gca,'clim',[-80,-30]);
% XLabels('Time (segundos)'); ylabel('Frecuencia Hz');



Vp1 = val.data_4(1046:end);
Vp2 = val.data_5(1046:end);
Vp3 = val.data_6(1046:end);

figure('Name','Diagnósticos Inteligentes: Dominio Frecuencial','NumberTitle','off');
figure(7);
        
T = timeStepNanos / (10^9); %1/Fs;             % Sampling period 
Fs = 1/T; %1000;            % Sampling frequency   
L = length(Ip1); %1500;             % Length of signal
t = (0:L-1)*T;        % Time vector

f = Fs*(0:(L/2))/L;

%%
subplot(3,1,1);

Y = fft(Ip1); % DIRECTAMENTE GRAFICA:  pwelch(val.data_0,[],[],[],Fs);
P2 = abs(Y/L);
P1 = P2(1:L/2+1);
P1(2:end-1) = 2*P1(2:end-1);

plot(f,P1,'r') 
hold on;

Y = fft(Vp1);
P2 = abs(Y/L);
P1 = P2(1:L/2+1);
P1(2:end-1) = 2*P1(2:end-1);

plot(f,P1,'b') 
hold off;
title('Phase 1 Spectrum');
legend('Current','Voltage');
xlabel('f (Hz)')
ylabel('|P1(f)|')


[pxx1,f] = pwelch(Ip1,[],[],[],Fs);
[pxx2,f] = pwelch(Ip2,[],[],[],Fs);
[pxx3,f] = pwelch(Ip3,[],[],[],Fs);

spectrum.Frequency = f;
spectrum.Phase1_I_log10PSD = log10(pxx1);
spectrum.Phase2_I_log10PSD = log10(pxx2);
spectrum.Phase3_I_log10PSD = log10(pxx3);

figure(8);
subplot(3,1,1);
plot(spectrum.Frequency,spectrum.Phase1_I_log10PSD);
subplot(3,1,2);
plot(spectrum.Frequency,spectrum.Phase2_I_log10PSD);
subplot(3,1,3);
plot(spectrum.Frequency,spectrum.Phase3_I_log10PSD);

jsonStr = jsonencode(spectrum);
fid = fopen('spectrum.json', 'w');
if fid == -1, error('Cannot create JSON file'); end
fwrite(fid, jsonStr, 'char');
fclose(fid);
