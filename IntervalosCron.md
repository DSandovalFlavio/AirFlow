# Intervalos basados en cron

Los intervalos basados en cron son una forma de especificar un intervalo de tiempo para ejecutar un trabajo. Los intervalos cron se basan en la especificación de cron, que es una especificación de intervalos de tiempo que se utiliza en muchos sistemas operativos. Los intervalos cron se pueden usar para ejecutar trabajos en intervalos regulares, como cada hora o cada día.

## Formato de intervalos cron estándar

Los intervalos cron se pueden especificar usando el formato de intervalos cron estándar. El formato de intervalos cron estándar se compone de cinco campos separados por espacios en blanco. Los campos son:

    -   minuto (0-59)
    -   hora (0-23)
    -   día del mes (1-31)
    -   mes (1-12)
    -   día de la semana (0 = domingo, 1 = lunes, 2 = martes, 3 = miércoles, 4 = jueves, 5 = viernes, 6 = sábado)

![cron](/imag/intervalos%20cron.png)

El formato de intervalos cron estándar se puede usar para especificar intervalos de tiempo que se ejecutan en un intervalo de tiempo específico. Por ejemplo, el intervalo de tiempo `0 0 * * *` se ejecuta todos los días a las 00:00.

Ejemplos de intervalos cron:

    -   `0 0 * * *` se ejecuta todos los días a las 00:00
    -   `0 0 * * 0` se ejecuta todos los domingos a las 00:00
    -   `0 0 1 * *` se ejecuta el primer día de cada mes a las 00:00
    -   `0 0 1 1 *` se ejecuta el primer día de enero a las 00:00
    -   `0 0 1 1 0` se ejecuta el primer día de enero de cada domingo a las 00:00
